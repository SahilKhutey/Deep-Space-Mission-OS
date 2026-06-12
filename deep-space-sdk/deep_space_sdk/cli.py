"""
Deep Space SDK CLI utility.
"""

import argparse
import sys
import json
from deep_space_sdk.client import DeepSpaceClient

def main():
    parser = argparse.ArgumentParser(description="Deep Space Engineering Ecosystem Command-Line Interface (CLI)")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # 1. Mission Planning
    plan_parser = subparsers.add_parser("plan", help="Plan a space mission and get delta-v timeline")
    plan_parser.add_argument("--origin", type=str, default="Earth", help="Origin planet/body")
    plan_parser.add_argument("--destination", type=str, required=True, help="Destination planet/body (e.g. Moon, Mars)")
    plan_parser.add_argument("--payload-mass", type=float, required=True, help="Payload mass in kg")
    plan_parser.add_argument("--json", action="store_true", help="Output results in JSON format")

    # 2. Cost Estimation
    cost_parser = subparsers.add_parser("cost", help="Estimate mission costs")
    cost_parser.add_argument("--dry-mass", type=float, required=True, help="Dry spacecraft mass in kg")
    cost_parser.add_argument("--propellant-mass", type=float, required=True, help="Propellant mass in kg")
    cost_parser.add_argument("--launch-cost", type=float, required=True, help="Launch vehicle cost in USD")
    cost_parser.add_argument("--ops-months", type=float, required=True, help="Mission operations duration in months")
    cost_parser.add_argument("--json", action="store_true", help="Output results in JSON format")

    # 3. Risk Assessment
    risk_parser = subparsers.add_parser("risk", help="Assess mission reliability and risk")
    risk_parser.add_argument("--duration", type=float, required=True, help="Mission duration in days")
    risk_parser.add_argument("--radiation", type=float, required=True, help="Solar radiation total dose in rads")
    risk_parser.add_argument("--components", type=int, required=True, help="Number of critical components")
    risk_parser.add_argument("--json", action="store_true", help="Output results in JSON format")

    # 4. Digital Twin
    twin_parser = subparsers.add_parser("twin", help="Analyze telemetry and predict anomalies using Digital Twin")
    twin_parser.add_argument("--state-name", type=str, required=True, help="Name of telemetry state variable (e.g. radiator_temp)")
    twin_parser.add_argument("--values", type=float, nargs="+", required=True, help="Space-separated list of historical values")
    twin_parser.add_argument("--forecast-steps", type=int, default=5, help="Number of steps to forecast forward")
    twin_parser.add_argument("--min-val", type=float, required=True, help="Lower safety threshold")
    twin_parser.add_argument("--max-val", type=float, required=True, help="Upper safety threshold")
    twin_parser.add_argument("--json", action="store_true", help="Output results in JSON format")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = DeepSpaceClient()

    if args.command == "plan":
        result = client.plan_mission(args.origin, args.destination, args.payload_mass)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"=== Mission Planning: {args.origin} -> {args.destination} ===")
            print(f"Feasibility: {result['feasible']}")
            print(f"Total Delta-V Required: {result['total_delta_v_km_s']:.2f} km/s")
            print(f"Propellant Fraction: {result['propellant_fraction']:.2%}")
            print("Timeline Events:")
            for event in result['timeline']:
                print(f"  - {event['event']}: {event['delta_v']:.2f} km/s")

    elif args.command == "cost":
        result = client.estimate_mission_cost(args.dry_mass, args.propellant_mass, args.launch_cost, args.ops_months)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print("=== Mission Cost Estimation ===")
            print(f"Dry Mass Cost: ${result['dry_mass_cost_usd']:,.2f}")
            print(f"Propellant Cost: ${result['propellant_cost_usd']:,.2f}")
            print(f"Operations Cost: ${result['ops_cost_usd']:,.2f}")
            print(f"----------------------------------------")
            print(f"Total Estimated Cost: ${result['total_cost_usd']:,.2f}")

    elif args.command == "risk":
        result = client.compute_mission_risk(args.duration, args.radiation, args.components)
        output = {"failure_probability": result, "reliability": 1.0 - result}
        if args.json:
            print(json.dumps(output, indent=2))
        else:
            print("=== Mission Risk & Reliability Assessment ===")
            print(f"Failure Probability: {result:.6f}")
            print(f"Reliability (Success Probability): {1.0 - result:.6f}")

    elif args.command == "twin":
        for v in args.values:
            client.log_twin_state(args.state_name, v)
        forecast = client.forecast_twin_state(args.state_name, args.forecast_steps)
        is_anomaly, val = client.predict_twin_anomaly(args.state_name, args.forecast_steps, (args.min_val, args.max_val))

        output = {
            "forecast_value": forecast,
            "is_anomaly": is_anomaly,
            "anomaly_value": val
        }

        if args.json:
            print(json.dumps(output, indent=2))
        else:
            print(f"=== Digital Twin Diagnostics: {args.state_name} ===")
            print(f"Forecast Value (in {args.forecast_steps} steps): {forecast:.4f}")
            status = "WARNING: ANOMALY PREDICTED" if is_anomaly else "NOMINAL"
            print(f"Status: {status}")
            if is_anomaly:
                print(f"Value exceeding threshold: {val:.4f} (Safety limits: [{args.min_val}, {args.max_val}])")

if __name__ == "__main__":
    main()
