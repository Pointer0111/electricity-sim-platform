# services/market_clear/fixed_cost_uniform.py

from schemas.simulation import DispatchResult


def clear_market_fixed_uniform(scenario, bid_data):
    demand = scenario["demand"]
    sorted_bids = sorted(bid_data.items(), key=lambda x: x[1].get('offer', x[1].get('price')))
    winners = sorted_bids[:demand]

    if len(winners) < demand:
        raise ValueError("Not enough bids to satisfy demand")

    clearing_price = winners[-1][1].get('offer', winners[-1][1].get('price'))
    dispatched = {}
    profits = {}

    for student, bid in bid_data.items():
        fixed_cost = bid.get("fixed_cost", 0.0)
        if student in dict(winners):
            dispatched[student] = True
            profit = clearing_price - bid["cost"] - fixed_cost
            profits[student] = round(profit, 2)
        else:
            dispatched[student] = False
            profits[student] = 0.0

    return DispatchResult(
        scenario_id=scenario["scenario_id"],
        clearing_price=clearing_price,
        dispatched=dispatched,
        profits=profits
    )
