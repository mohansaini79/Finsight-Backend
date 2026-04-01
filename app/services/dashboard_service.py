from app.database import financial_records_collection


def get_dashboard_summary() -> dict:
    match_stage = {"$match": {"is_deleted": False}}

    # Total income/expense
    totals_pipeline = [
        match_stage,
        {"$group": {"_id": "$type", "total": {"$sum": "$amount"}}},
    ]
    totals_raw = list(financial_records_collection.aggregate(totals_pipeline))
    totals = {item["_id"]: float(item["total"]) for item in totals_raw}
    total_income = round(totals.get("income", 0.0), 2)
    total_expense = round(totals.get("expense", 0.0), 2)

    # Category-wise totals (income adds, expense subtracts for a useful net view per category)
    category_pipeline = [
        match_stage,
        {
            "$group": {
                "_id": "$category",
                "total": {
                    "$sum": {
                        "$cond": [{"$eq": ["$type", "income"]}, "$amount", {"$multiply": ["$amount", -1]}]
                    }
                },
            }
        },
        {"$sort": {"total": -1}},
    ]
    category_raw = list(financial_records_collection.aggregate(category_pipeline))
    category_wise_totals = {item["_id"]: round(float(item["total"]), 2) for item in category_raw}

    # Monthly grouping by YYYY-MM
    monthly_pipeline = [
        match_stage,
        {
            "$group": {
                "_id": {
                    "year": {"$year": "$date"},
                    "month": {"$month": "$date"},
                    "type": "$type",
                },
                "total": {"$sum": "$amount"},
            }
        },
        {"$sort": {"_id.year": 1, "_id.month": 1}},
    ]
    monthly_raw = list(financial_records_collection.aggregate(monthly_pipeline))

    month_map: dict[str, dict] = {}
    for item in monthly_raw:
        y = item["_id"]["year"]
        m = item["_id"]["month"]
        t = item["_id"]["type"]
        key = f"{y}-{m:02d}"
        if key not in month_map:
            month_map[key] = {"month": key, "income": 0.0, "expense": 0.0}
        month_map[key][t] = round(float(item["total"]), 2)

    monthly_summary = list(month_map.values())

    recent_cursor = (
        financial_records_collection.find({"is_deleted": False})
        .sort("date", -1)
        .limit(5)
    )
    recent_transactions = []
    for tx in recent_cursor:
        recent_transactions.append(
            {
                "id": str(tx["_id"]),
                "amount": float(tx["amount"]),
                "type": tx["type"],
                "category": tx["category"],
                "date": tx["date"].isoformat(),
                "notes": tx.get("notes", ""),
                "created_by": tx["created_by"],
            }
        )

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "net_balance": round(total_income - total_expense, 2),
        "category_wise_totals": category_wise_totals,
        "monthly_summary": monthly_summary,
        "recent_transactions": recent_transactions,
    }