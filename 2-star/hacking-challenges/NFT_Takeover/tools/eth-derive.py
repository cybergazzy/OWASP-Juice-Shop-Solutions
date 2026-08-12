# Dedicated to Cybergazzy
from eth_account import Account
import getpass

# Enable HD Wallet features in eth-account
Account.enable_unaudited_hdwallet_features()

def derive_cybergazzy_eth_key(mnemonic_phrase: str, account_index: int = 0) -> dict:
    cleaned_words = " ".join(mnemonic_phrase.strip().lower().split())
    words = cleaned_words.split()

    if len(words) != 12:
        raise ValueError(f"Expected 12 words, but got {len(words)}.")

    derivation_path = f"m/44'/60'/0'/0/{account_index}"
    account = Account.from_mnemonic(cleaned_words, account_path=derivation_path)

    return {
        "address": account.address,
        "private_key": account.key.hex(),
        "derivation_path": derivation_path
    }

if __name__ == "__main__":
    print("==================================================")
    print("      CYBERGAZZY ETHEREUM KEY DERIVATION          ")
    print("==================================================")

    # Prompt for the seed phrase at runtime (input is hidden for privacy)
    user_seed = getpass.getpass("Paste/Type your 12-word seed phrase (input hidden): ")

    # Fallback to visible input if terminal doesn't support getpass echo suppression
    if not user_seed.strip():
        user_seed = input("Enter your 12-word seed phrase: ")

    try:
        wallet_info = derive_cybergazzy_eth_key(user_seed)
        print("\n--- Derivation Complete ---")
        print(f"Derivation Path : {wallet_info['derivation_path']}")
        print(f"Ethereum Address: {wallet_info['address']}")
        print(f"Private Key     : {wallet_info['private_key']}")
    except Exception as e:
        print(f"\nError: {e}")
