"""Price math for desynth profit tracking."""


def compute_profit(earned, cost):
    """Profit = gil earned minus gil spent."""
    return earned - cost


def entry_profit(entry):
    return compute_profit(float(entry.get("earned", 0)), float(entry.get("cost", 0)))


def aggregate_by_item(entries):
    result = {}
    for entry in entries:
        item = str(entry.get("item", "Unknown"))
        earned = float(entry.get("earned", 0))
        cost = float(entry.get("cost", 0))
        profit = compute_profit(earned, cost)
        agg = result.setdefault(
            item,
            {"count": 0, "earned": 0.0, "cost": 0.0, "profit": 0.0},
        )
        agg["count"] += 1
        agg["earned"] += earned
        agg["cost"] += cost
        agg["profit"] += profit
    for agg in result.values():
        agg["margin"] = (agg["profit"] / agg["earned"] * 100) if agg["earned"] else 0.0
    return result


def totals(entries):
    earned = sum(float(e.get("earned", 0)) for e in entries)
    cost = sum(float(e.get("cost", 0)) for e in entries)
    return {"earned": earned, "cost": cost, "profit": compute_profit(earned, cost)}
