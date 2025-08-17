from colorama import Fore, Style, init

init(autoreset=True)

FULLWIDTH_DIGITS = ["０","１","２","３","４","５","６","７","８"]

# Example: show digits 1, 2, 3 in red, green, grey
print(f"{Fore.RED}{FULLWIDTH_DIGITS[1]}{Style.RESET_ALL} "
      f"{Fore.GREEN}{FULLWIDTH_DIGITS[2]}{Style.RESET_ALL} "
      f"{Fore.LIGHTBLACK_EX}{FULLWIDTH_DIGITS[3]}{Style.RESET_ALL}")