import json

def handle_create_general_ledger(accountName: str, initialBalance: float):
    if not accountName or initialBalance == 0.0:
        return json.dumps(
            {
                "success": False,
                "status": "Failed to create the general ledger. Both accountName and initialBalance must be provided."
            }
        )
    else:
        try:
            return json.dumps(
                {
                    "accountName": accountName,
                    "initialBalance": initialBalance,
                    "success": True,
                    "status": "Created the general ledger"
                }
            )
        except Exception as ex:
            return json.dumps(
                {
                    "success": False,
                    "status": "An error occurred while creating the general ledger."
                }
            )

def generate_balance_sheet():
    guidance = [
        "Go to the 'Reports section'",
        "Select 'Balance Sheet'",
        "Choose the date range",
        "Click 'Generate Report'"
    ]
    return json.dumps(
        {
            "guidance": guidance,
            "success": True,
            "status": "I cannot generate the balance sheet report directly. Follow the guidance steps"
        }
    )