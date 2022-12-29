from tqdm import tqdm
import pathlib
import pikepdf
import typing as tp


class PathNamesConfig:
    @property
    def wordlist(self) -> str:
        file_name = "wordlist.txt"
        return str(self._files_path.joinpath(file_name))

    @property
    def pdf(self) -> str:
        file_name = "secret-document.pdf"
        return str(self._files_path.joinpath(file_name))

    @property
    def _files_path(self) -> pathlib.Path:
        return self._this_script_path.parent.joinpath("files")

    @property
    def _this_script_path(self) -> pathlib.Path:
        return pathlib.Path(__file__).parent.absolute()


class PdfCracker:
    def __init__(self, passwords: tp.List[str], path_names: PathNamesConfig):
        self._passwords = passwords
        self._path_names = path_names

    def get_pdf_password(self) -> tp.Optional[str]:
        for password in tqdm(self._passwords, "Decrypting PDF"):
            print(f"Checking password: {password}")
            if self._is_password_correct(password):
                return password

    def _is_password_correct(self, password: str) -> bool:
        try:
            with pikepdf.open(self._path_names.pdf, password=password):
                return True
        except pikepdf._qpdf.PasswordError:
            return False


def run():
    path_names = PathNamesConfig()
    passwords = get_passwords(path_names)
    password = PdfCracker(passwords, path_names).get_pdf_password()
    if password is None:
        print(f"\n[-] No password found")
    else:
        print(f"\n[+] Password found: {password}")


def get_passwords(path_names: PathNamesConfig) -> tp.List[str]:
    return [line.strip() for line in open(path_names.wordlist)]


if __name__ == "__main__":
    run()
