#

servers = ["web-01", "db-01", "web-01", "app-01", "db-01", "app-02"]

unique_sorted = sorted(set(servers))
print(unique_sorted)

#

import argparse
import json
import logging
import os
import sys

# ── Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("server_dedup.log")
    ]
)
logger = logging.getLogger(__name__)


def remove_duplicates_and_sort(servers: list) -> list:
    """
    Removes duplicate server names and sorts alphabetically.

    Args:
        servers: list of server names with possible duplicates
    Returns:
        list: deduplicated and alphabetically sorted server names
    Raises:
        ValueError: if servers list is empty
        TypeError: if servers is not a list
    """
    # ── Validate input type
    if not isinstance(servers, list):
        raise TypeError(
            f"Expected list, got: {type(servers).__name__}"
        )

    # ── Validate list is not empty
    if len(servers) == 0:
        raise ValueError("Server list is empty")

    logger.info(f"Total servers before dedup: {len(servers)}")

    # ── Find duplicates before removing
    seen = set()
    duplicates = set()
    for server in servers:
        if server in seen:
            duplicates.add(server)
        seen.add(server)

    if duplicates:
        logger.warning(
            f"Duplicate servers found: {sorted(duplicates)}"
        )
    else:
        logger.info("No duplicates found")

    # ── Remove duplicates using set + sort
    unique_sorted = sorted(set(servers))

    logger.info(f"Total servers after dedup: {len(unique_sorted)}")
    logger.info(f"Removed {len(servers) - len(unique_sorted)} duplicates")

    return unique_sorted


def read_servers_from_file(filepath: str) -> list:
    """
    Reads server names from a file — one server per line
    or a JSON array file.

    Args:
        filepath: path to file containing server names
    Returns:
        list: server names read from file
    Raises:
        FileNotFoundError: if file does not exist
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: '{filepath}'")

    logger.info(f"Reading servers from file: {filepath}")

    # ── Handle JSON file
    if filepath.endswith(".json"):
        with open(filepath, "r") as f:
            servers = json.load(f)
        logger.info(f"Loaded {len(servers)} servers from JSON")
        return servers

    # ── Handle plain text file (one server per line)
    with open(filepath, "r") as f:
        servers = [
            line.strip()
            for line in f.readlines()
            if line.strip()  # skip empty lines
        ]

    logger.info(f"Loaded {len(servers)} servers from text file")
    return servers


def save_output(servers: list, output_file: str) -> None:
    """
    Saves deduplicated server list to output file.

    Args:
        servers: list of server names to save
        output_file: path to save output
    """
    with open(output_file, "w") as f:
        for server in servers:
            f.write(f"{server}\n")

    logger.info(f"Saved {len(servers)} servers to: {output_file}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Remove duplicate server names and sort alphabetically"
    )

    # ── Input group — either --servers or --file
    input_group = parser.add_mutually_exclusive_group(required=True)

    input_group.add_argument(
        "--servers",
        nargs="+",
        help="Space separated list of server names"
    )
    input_group.add_argument(
        "--file",
        help="Path to file containing server names (txt or json)"
    )

    parser.add_argument(
        "--output",
        help="Save result to output file (optional)"
    )

    parser.add_argument(
        "--show-duplicates",
        action="store_true",
        help="Show which servers were duplicates"
    )

    return parser.parse_args()


def main():
    args = parse_args()

    try:
        # ── Get servers from argument or file
        if args.servers:
            servers = args.servers
            logger.info(f"Servers provided via CLI: {servers}")
        else:
            servers = read_servers_from_file(args.file)

        # ── Find duplicates before processing (for display)
        duplicates = [s for s in servers if servers.count(s) > 1]
        unique_duplicates = sorted(set(duplicates))

        # ── Process
        result = remove_duplicates_and_sort(servers)

        # ── Print results
        print("\n" + "─" * 50)
        print(f" Original count  : {len(servers)}")
        print(f" After dedup     : {len(result)}")
        print(f" Duplicates found: {len(servers) - len(result)}")
        print("─" * 50)

        if args.show_duplicates and unique_duplicates:
            print(f"\n Duplicate servers:")
            for s in unique_duplicates:
                print(f"   → {s}")

        print(f"\n Sorted unique servers:")
        for server in result:
            print(f"   ✓ {server}")
        print()

        # ── Save to file if requested
        if args.output:
            save_output(result, args.output)
            print(f" Saved to: {args.output}\n")

    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        sys.exit(1)

    except TypeError as e:
        logger.error(f"Type error: {e}")
        sys.exit(1)

    except ValueError as e:
        logger.error(f"Value error: {e}")
        sys.exit(1)

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()