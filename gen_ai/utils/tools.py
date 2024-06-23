tools = [
    {
        "type": "function",
        "function": {
            "name": "handle_create_general_ledger",
            "description": "Create a general ledger",
            "parameters": {
                "type": "object",
                "properties": {
                    "accountName": {
                        "type": "string",
                        "description": "The account name of the user to whom the ledger will be created",
                    },
                    "initialBalance": {
                        "type": "number",
                        "description": "The initial balance",
                    }
                },
                "required": ["accountName", "initialBalance"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "generate_balance_sheet",
            "description": "generating a balance sheet report",
            "parameters": {
                "type": "object",
                "properties": {
                }
            },
        },
    }
]