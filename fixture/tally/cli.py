"""Command-line entry point for tally.

Subcommands:
    add     record an expense
    report  print category totals for a month (optionally one category)
    export  write all expenses to CSV
    budget  show spending against configured category budgets

The default store lives at ./tally.json; override it with --store.
"""

import argparse
import sys

from tally import report as report_mod
from tally import store as store_mod
from tally.config import DEFAULT_CURRENCY
from tally.utils import month_key, parse_date

DEFAULT_STORE = "tally.json"


def _load(args):
    return store_mod.load(args.store)


def cmd_add(args):
    data = _load(args)
    # normalize the date so we fail early on a bad value
    date = parse_date(args.date).isoformat()
    record = store_mod.add_expense(
        data,
        date=date,
        amount=args.amount,
        currency=args.currency,
        category=args.category,
        note=args.note or "",
    )
    store_mod.save(args.store, data)
    print(
        "added #{id}: {amount_usd:.2f} USD  {category}  {date}".format(**record)
    )
    return 0


def cmd_report(args):
    data = _load(args)
    text = report_mod.format_report(
        store_mod.all_expenses(data), month=args.month, category=args.category
    )
    print(text)
    return 0


def cmd_list(args):
    data = _load(args)
    rows = report_mod.filter_expenses(
        store_mod.all_expenses(data), month=args.month, category=args.category
    )
    print(report_mod.format_expense_list(rows))
    return 0


def cmd_export(args):
    data = _load(args)
    csv_text = report_mod.to_csv(store_mod.all_expenses(data))
    if args.out:
        with open(args.out, "w") as fh:
            fh.write(csv_text)
        print("wrote {}".format(args.out))
    else:
        sys.stdout.write(csv_text)
    return 0


def cmd_stats(args):
    data = _load(args)
    stats = report_mod.overall_stats(store_mod.all_expenses(data))
    if stats["count"] == 0:
        print("no expenses recorded")
        return 0
    print("expenses : {count}".format(**stats))
    print("total    : {total:.2f} USD".format(**stats))
    print("average  : {average:.2f} USD".format(**stats))
    print("span     : {first_date} .. {last_date}".format(**stats))
    return 0


def cmd_budget(args):
    data = _load(args)
    rows = report_mod.budget_status(store_mod.all_expenses(data), month=args.month)
    print("Budget for {}".format(args.month))
    for row in rows:
        print(
            "{category:<14} {spent:>8.2f} / {budget:>8.2f} USD  {state}".format(**row)
        )
    return 0


def build_parser():
    parser = argparse.ArgumentParser(prog="tally", description="Personal expense tracker.")
    parser.add_argument("--store", default=DEFAULT_STORE, help="path to the JSON store")
    sub = parser.add_subparsers(dest="command")

    p_add = sub.add_parser("add", help="record an expense")
    p_add.add_argument("amount", type=float)
    p_add.add_argument("category")
    p_add.add_argument("--currency", default=DEFAULT_CURRENCY)
    p_add.add_argument("--date", default=None, help="YYYY-MM-DD (default: today)")
    p_add.add_argument("--note", default="")
    p_add.set_defaults(func=cmd_add)

    p_report = sub.add_parser("report", help="category totals for a month")
    p_report.add_argument("--month", default=None, help="YYYY-MM")
    p_report.add_argument("--category", default=None)
    p_report.set_defaults(func=cmd_report)

    p_list = sub.add_parser("list", help="list individual expenses")
    p_list.add_argument("--month", default=None, help="YYYY-MM")
    p_list.add_argument("--category", default=None)
    p_list.set_defaults(func=cmd_list)

    p_export = sub.add_parser("export", help="export all expenses to CSV")
    p_export.add_argument("--out", default=None, help="file to write (default: stdout)")
    p_export.set_defaults(func=cmd_export)

    p_stats = sub.add_parser("stats", help="overall summary statistics")
    p_stats.set_defaults(func=cmd_stats)

    p_budget = sub.add_parser("budget", help="spending vs configured budgets")
    p_budget.add_argument("--month", required=True, help="YYYY-MM")
    p_budget.set_defaults(func=cmd_budget)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "command", None):
        parser.print_help()
        return 1
    if args.command == "add" and args.date is None:
        import datetime

        args.date = datetime.date.today().isoformat()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
