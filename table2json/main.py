import sys

from table2json.core.management.utility import ManagementUtility


def main():
    """Main"""

    utility = ManagementUtility(sys.argv)
    utility.execute()
