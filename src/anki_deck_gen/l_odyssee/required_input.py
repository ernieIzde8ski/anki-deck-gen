from dataclasses import dataclass

__all__ = ["required_input"]


@dataclass
class RequiredInput:
    is_notified: bool = False

    def print_notice(self, force: bool = False):
        if force is False and self.is_notified is True:
            return
        print("Shortcuts:")
        print("\t<C-D>: save and quit")
        print("\t<C-C>: quit without saving")
        print("\tinput 'NULL': ignore current note")
        print("\tinput other: put text on back of note")
        print()
        self.is_notified = True

    def __call__(self, prompt: str):
        """Get input. Does not return an empty string."""
        self.print_notice()
        res = ""
        while True:
            res += input(prompt).strip()
            if not res:
                continue

            rev = reversed(res)
            backslash_count = 0
            for c in rev:
                if c == "\\":
                    backslash_count += 1
                else:
                    break

            if backslash_count % 2 == 0:
                return res
            else:
                res = res[: len(res) - 1].rstrip() + "\n"


required_input = RequiredInput()
