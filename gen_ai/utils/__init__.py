import functools
from .functions import handle_create_general_ledger, generate_balance_sheet

names_to_functions = {
    'handle_create_general_ledger': functools.partial(handle_create_general_ledger),
    'generate_balance_sheet': functools.partial(generate_balance_sheet)
}