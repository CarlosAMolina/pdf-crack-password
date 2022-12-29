from tqdm import tqdm
import pikepdf
import typing as tp


def run():
    passwords = get_passwords()
    password = get_pdf_password(passwords)
    if password is None:
        print(f"\n[-] No password found")
    else:
        print(f"\n[+] Password found: {password}")


def get_passwords() -> tp.List[str]:
    return [line.strip() for line in open("files/wordlist.txt")]


def get_pdf_password(passwords: tp.List[str]) -> tp.Optional[str]:
    for password in tqdm(passwords, "Decrypting PDF"):
        print(f"Checking password: {password}")
        if is_password_correct(password):
            return password


def is_password_correct(password: str) -> bool:
    try:
        with pikepdf.open("files/secret-document.pdf", password=password) as pdf:
            return True
    except pikepdf._qpdf.PasswordError as e:
        return False


if __name__ == "__main__":
    run()
