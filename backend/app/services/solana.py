import httpx
from decimal import Decimal

from app.config import get_settings

settings = get_settings()


class SolanaService:
    """Service for Solana transaction verification."""

    @staticmethod
    async def verify_transaction(
        transaction_signature: str,
        expected_amount: Decimal | None = None,
        expected_recipient: str | None = None,
    ) -> dict:
        """
        Verify a Solana transaction.

        Args:
            transaction_signature: The Solana transaction signature to verify
            expected_amount: Optional expected amount in lamports
            expected_recipient: Optional expected recipient wallet address

        Returns:
            dict with keys:
                - verified: bool
                - confirmed: bool
                - amount: Decimal (in lamports)
                - recipient: str
                - error: str (if verification failed)
        """
        rpc_url = settings.solana_rpc_url

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                # Get transaction details
                response = await client.post(
                    rpc_url,
                    json={
                        "jsonrpc": "2.0",
                        "id": 1,
                        "method": "getTransaction",
                        "params": [
                            transaction_signature,
                            {
                                "encoding": "jsonParsed",
                                "maxSupportedTransactionVersion": 0,
                            },
                        ],
                    },
                )
                response.raise_for_status()
                result = response.json()

                if "error" in result:
                    return {
                        "verified": False,
                        "confirmed": False,
                        "error": result["error"].get("message", "Unknown RPC error"),
                    }

                transaction_data = result.get("result")
                if not transaction_data:
                    return {
                        "verified": False,
                        "confirmed": False,
                        "error": "Transaction not found",
                    }

                # Check if transaction is confirmed
                if transaction_data.get("meta", {}).get("err"):
                    return {
                        "verified": False,
                        "confirmed": True,
                        "error": f"Transaction failed: {transaction_data['meta']['err']}",
                    }

                # Extract transaction details
                transaction = transaction_data.get("transaction", {})
                message = transaction.get("message", {})
                account_keys = message.get("accountKeys", [])

                # Extract transfer amount and recipient from instructions
                # This is a simplified version - you may need to adjust based on your transaction structure
                meta = transaction_data.get("meta", {})
                pre_balances = meta.get("preBalances", [])
                post_balances = meta.get("postBalances", [])
                pre_token_balances = meta.get("preTokenBalances", [])
                post_token_balances = meta.get("postTokenBalances", [])

                # Calculate SOL transfer (simplified - assumes single transfer)
                # In production, you'd parse the instructions more carefully
                amount_lamports = Decimal(0)
                recipient = None

                # Try to find the recipient by looking at balance changes
                # This is simplified - adjust based on your actual transaction structure
                if account_keys and len(pre_balances) == len(post_balances):
                    for i, (pre, post) in enumerate(zip(pre_balances, post_balances)):
                        if post > pre:
                            amount_lamports = Decimal(post - pre)
                            if i < len(account_keys):
                                recipient = account_keys[i].get("pubkey")
                            break

                # Verify expected values if provided
                if expected_amount and amount_lamports != expected_amount:
                    return {
                        "verified": False,
                        "confirmed": True,
                        "error": f"Amount mismatch: expected {expected_amount}, got {amount_lamports}",
                    }

                # Verify recipient if provided
                if expected_recipient:
                    # Check if recipient matches expected (case-insensitive)
                    if recipient and recipient.lower() != expected_recipient.lower():
                        return {
                            "verified": False,
                            "confirmed": True,
                            "error": f"Recipient mismatch: expected {expected_recipient}, got {recipient}",
                        }

                return {
                    "verified": True,
                    "confirmed": True,
                    "amount": amount_lamports,
                    "recipient": recipient,
                }

        except httpx.TimeoutException:
            return {
                "verified": False,
                "confirmed": False,
                "error": "Request timeout while verifying transaction",
            }
        except httpx.HTTPStatusError as e:
            return {
                "verified": False,
                "confirmed": False,
                "error": f"HTTP error: {e.response.status_code}",
            }
        except Exception as e:
            return {
                "verified": False,
                "confirmed": False,
                "error": f"Verification error: {str(e)}",
            }

    @staticmethod
    def convert_lamports_to_sol(lamports: Decimal) -> Decimal:
        """Convert lamports to SOL."""
        return lamports / Decimal(1_000_000_000)

    @staticmethod
    def convert_sol_to_lamports(sol: Decimal) -> Decimal:
        """Convert SOL to lamports."""
        return sol * Decimal(1_000_000_000)
