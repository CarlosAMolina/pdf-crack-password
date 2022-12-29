from tqdm import tqdm
import pikepdf
import typing as tp


class PathsConfig:
    @property
    def wordlist(self) -> str:
        return "files/wordlist.txt"

    @property
    def pdf(self) -> str:
        return "files/secret-document.pdf"


class PdfCracker:
    def __init__(self, passwords: tp.List[str], paths_config: PathsConfig):
        self._passwords = passwords
        self._paths_config = paths_config

    def get_pdf_password(self) -> tp.Optional[str]:
        for password in tqdm(self._passwords, "Decrypting PDF"):
            print(f"Checking password: {password}")
            if self._is_password_correct(password):
                return password

    def _is_password_correct(self, password: str) -> bool:
        try:
            with pikepdf.open(self._paths_config.pdf, password=password):
                return True
        except pikepdf._qpdf.PasswordError:
            return False


def run():
    paths_config = PathsConfig()
    passwords = get_passwords(paths_config)
    password = PdfCracker(passwords, paths_config).get_pdf_password()
    if password is None:
        print(f"\n[-] No password found")
    else:
        print(f"\n[+] Password found: {password}")


def get_passwords(paths_config: PathsConfig) -> tp.List[str]:
    return [line.strip() for line in open(paths_config.wordlist)]


if __name__ == "__main__":
    run()
