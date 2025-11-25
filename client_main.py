"""
Terminal Client for Intelligence Reporting System

This client communicates with the API server via HTTP requests.
It no longer accesses the database directly.

Architecture:
Terminal Client (this file) -> HTTP API -> Services -> DAL -> Database
"""
from client import APIClient
from utils import save_current_agent, load_current_agent, clear_current_agent


# Global variable to store current logged-in agent
current_agent = None

# API Client instance
api_client = APIClient()


def print_header():
    """Print application header"""
    print("\n" + "=" * 60)
    print("Intelligence Reporting System - Terminal Client")
    print("Terrorist Intelligence Tracking System")
    print("=" * 60)


def print_menu():
    """Print main menu"""
    print("\n" + "-" * 60)
    print("Main Menu:")
    print("-" * 60)
    if current_agent:
        print(f"Logged in as: {current_agent['name']} ({current_agent['username']})")
        print()
    print("1. Agent Login")
    print("2. Execute Free SQL")
    print("3. Create Intelligence Report")
    print("4. Delete Intelligence Report")
    print("5. Search Reports by Keywords")
    print("6. Search Reports by Terrorist")
    print("7. Search Dangerous Terrorists")
    print("8. Search Super Dangerous Terrorists")
    print("9. Exit")
    print("-" * 60)


def agent_login():
    """Handle agent login via HTTP API"""
    global current_agent
    
    print("\n--- Agent Login ---")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    
    try:
        # Send login request to API
        agent_data = api_client.login(username, password)
        
        current_agent = {
            "id": agent_data["id"],
            "username": agent_data["username"],
            "name": agent_data["name"]
        }
        save_current_agent(agent_data["id"], agent_data["username"], agent_data["name"])
        print(f"\n✓ Login successful! Welcome {agent_data['name']}")
    except Exception as e:
        print(f"\n❌ Login failed: {str(e)}")
        
        # Ask if user wants to create a new agent
        create_new = input("Do you want to create a new agent? (y/n): ").strip().lower()
        if create_new == 'y':
            name = input("Full Name: ").strip()
            if name:
                try:
                    new_agent = api_client.register(name, username, password)
                    current_agent = {
                        "id": new_agent["id"],
                        "username": new_agent["username"],
                        "name": new_agent["name"]
                    }
                    save_current_agent(new_agent["id"], new_agent["username"], new_agent["name"])
                    print(f"\n✓ New agent created and logged in successfully!")
                except Exception as e:
                    print(f"\n❌ Registration failed: {str(e)}")


def execute_free_sql():
    """Execute free SQL query via HTTP API"""
    print("\n--- Execute Free SQL ---")
    print("Enter SQL query (or 'back' to return):")
    sql_query = input("> ").strip()
    
    if sql_query.lower() == 'back':
        return
    
    try:
        # Send SQL execution request to API
        result = api_client.execute_sql(sql_query)
        
        if result.get("success"):
            if "results" in result:
                rows = result["results"]
                print(f"\n✓ Found {len(rows)} results:")
                for row in rows:
                    print(f"  {row}")
            else:
                print(f"\n✓ {result.get('message', 'Query executed successfully')}")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


def create_intelligence_report():
    """Create a new intelligence report via HTTP API"""
    if not current_agent:
        print("\n❌ You must login first!")
        return
    
    print("\n--- Create New Intelligence Report ---")
    
    # Get terrorist ID
    print("\nOption 1: Enter existing terrorist ID")
    print("Option 2: Create new terrorist")
    choice = input("Choose option (1/2): ").strip()
    
    terrorist_id = None
    
    if choice == '1':
        try:
            terrorist_id = int(input("Terrorist ID: ").strip())
        except ValueError:
            print("❌ Invalid ID")
            return
    elif choice == '2':
        terrorist_name = input("Terrorist Name: ").strip()
        if not terrorist_name:
            print("❌ Terrorist name is required")
            return
        
        affiliation = input("Affiliation (optional): ").strip() or None
        location = input("Location (optional): ").strip() or None
        
        try:
            terrorist_data = api_client.create_terrorist(terrorist_name, affiliation, location)
            terrorist_id = terrorist_data["id"]
            print(f"\n✓ Terrorist created with ID: {terrorist_id}")
        except Exception as e:
            print(f"\n❌ Failed to create terrorist: {str(e)}")
            return
    else:
        print("❌ Invalid option")
        return
    
    # Get report content
    print("\nEnter report content:")
    content = input("> ").strip()
    
    if not content:
        print("❌ Report content is required")
        return
    
    # Create the report via API
    try:
        report_data = api_client.create_report(content, current_agent['id'], terrorist_id)
        print(f"\n✓ Intelligence report created successfully! Report ID: {report_data['id']}")
    except Exception as e:
        print(f"\n❌ Failed to create report: {str(e)}")


def delete_intelligence_report():
    """Delete an intelligence report via HTTP API"""
    if not current_agent:
        print("\n❌ You must login first!")
        return
    
    print("\n--- Delete Intelligence Report ---")
    
    try:
        report_id = int(input("Enter report ID to delete: ").strip())
    except ValueError:
        print("❌ Invalid ID")
        return
    
    confirm = input(f"\nAre you sure you want to delete report {report_id}? (y/n): ").strip().lower()
    if confirm == 'y':
        try:
            result = api_client.delete_report(report_id, current_agent['id'])
            print(f"\n✓ {result.get('message', 'Report deleted successfully')}")
        except Exception as e:
            print(f"\n❌ Failed to delete report: {str(e)}")


def search_reports_by_keywords():
    """Search reports by keywords via HTTP API"""
    print("\n--- Search Reports by Keywords ---")
    
    keyword = input("Enter keyword: ").strip()
    if not keyword:
        print("❌ Keyword is required")
        return
    
    try:
        reports = api_client.search_reports_by_text(keyword)
        
        if not reports:
            print(f"\n❌ No reports found containing '{keyword}'")
            return
        
        print(f"\n✓ Found {len(reports)} reports:")
        for report in reports:
            print(f"\n  Report ID: {report['id']}")
            print(f"  Terrorist: {report.get('terrorist_name', 'Unknown')}")
            print(f"  Agent: {report.get('agent_name', 'Unknown')}")
            print(f"  Date: {report['created_at'][:19]}")
            print(f"  Content: {report['content'][:150]}...")
    except Exception as e:
        print(f"\n❌ Search failed: {str(e)}")


def search_reports_by_terrorist_menu():
    """Search reports by terrorist via HTTP API"""
    print("\n--- Search Reports by Terrorist ---")
    
    try:
        terrorist_id = int(input("Enter terrorist ID: ").strip())
    except ValueError:
        print("❌ Invalid ID")
        return
    
    try:
        result = api_client.search_reports_by_terrorist(terrorist_id)
        
        print(f"\n✓ Terrorist: {result['terrorist_name']}")
        print(f"✓ Found {result['total_reports']} total reports")
        
        if result['total_reports'] == 0:
            return
        
        reports = result['reports']
        print(f"\nShowing first {len(reports)} reports:")
        
        for report in reports:
            print(f"\n  Report ID: {report['id']}")
            print(f"  Agent: {report.get('agent_name', 'Unknown')}")
            print(f"  Date: {report['created_at'][:19]}")
            print(f"  Content: {report['content'][:150]}...")
    except Exception as e:
        print(f"\n❌ Search failed: {str(e)}")


def search_dangerous_terrorists():
    """Search for dangerous terrorists (>5 reports) via HTTP API"""
    print("\n--- Search Dangerous Terrorists ---")
    print("Terrorists with more than 5 reports\n")
    
    try:
        results = api_client.get_dangerous_terrorists()
        
        if not results:
            print("❌ No dangerous terrorists found")
            return
        
        print(f"✓ Found {len(results)} dangerous terrorists:\n")
        for terrorist in results:
            print(f"  Name: {terrorist['terrorist_name']}")
            print(f"  ID: {terrorist['terrorist_id']}")
            print(f"  Number of reports: {terrorist['report_count']}")
            if terrorist.get('affiliation'):
                print(f"  Affiliation: {terrorist['affiliation']}")
            if terrorist.get('location'):
                print(f"  Location: {terrorist['location']}")
            print()
    except Exception as e:
        print(f"\n❌ Search failed: {str(e)}")


def search_super_dangerous_terrorists():
    """Search for super dangerous terrorists (>10 reports + weapon keywords) via HTTP API"""
    print("\n--- Search Super Dangerous Terrorists ---")
    print("Terrorists with more than 10 reports and weapon keywords\n")
    
    try:
        results = api_client.get_super_dangerous_terrorists()
        
        if not results:
            print("❌ No super dangerous terrorists found")
            return
        
        print(f"✓ Found {len(results)} super dangerous terrorists:\n")
        for terrorist in results:
            print(f"  Name: {terrorist['terrorist_name']}")
            print(f"  ID: {terrorist['terrorist_id']}")
            print(f"  Number of reports: {terrorist['report_count']}")
            if terrorist.get('affiliation'):
                print(f"  Affiliation: {terrorist['affiliation']}")
            if terrorist.get('location'):
                print(f"  Location: {terrorist['location']}")
            print()
    except Exception as e:
        print(f"\n❌ Search failed: {str(e)}")


def main():
    """Main application loop"""
    global current_agent
    
    print_header()
    print("\nNote: Make sure the API server is running on http://localhost:8000")
    print("Start server with: python server.py")
    
    # Load current agent if exists
    saved_agent = load_current_agent()
    if saved_agent:
        current_agent = saved_agent
        print(f"\n✓ Auto-login: {current_agent['name']}")
    
    # Main loop
    while True:
        print_menu()
        choice = input("\nChoose option: ").strip()
        
        if choice == '1':
            agent_login()
        elif choice == '2':
            execute_free_sql()
        elif choice == '3':
            create_intelligence_report()
        elif choice == '4':
            delete_intelligence_report()
        elif choice == '5':
            search_reports_by_keywords()
        elif choice == '6':
            search_reports_by_terrorist_menu()
        elif choice == '7':
            search_dangerous_terrorists()
        elif choice == '8':
            search_super_dangerous_terrorists()
        elif choice == '9':
            print("\n👋 Goodbye!")
            break
        else:
            print("\n❌ Invalid option")


if __name__ == "__main__":
    main()
