from typing import Optional, List
from sqlmodel import Session, select, col, func
from app.models import Report, Agent, Terrorist
from db.database import get_engine


def create_report(content: str, agent_id: int, terrorist_id: int) -> Report:
    """CREATE - Add a new report to the database"""
    engine = get_engine()
    with Session(engine) as session:
        report = Report(content=content, agent_id=agent_id, terrorist_id=terrorist_id)
        session.add(report)
        session.commit()
        session.refresh(report)
        print(f"✓ Created new intelligence report (ID: {report.id})")
        return report


def get_report_by_id(report_id: int) -> Optional[Report]:
    """READ - Get a report by ID"""
    engine = get_engine()
    with Session(engine) as session:
        return session.get(Report, report_id)


def get_all_reports():
    """READ - Get all reports"""
    engine = get_engine()
    with Session(engine) as session:
        statement = select(Report)
        reports = session.exec(statement).all()
        return reports


def get_reports_by_agent(agent_id: int):
    """READ - Get all reports written by a specific agent"""
    engine = get_engine()
    with Session(engine) as session:
        statement = select(Report).where(Report.agent_id == agent_id)
        reports = session.exec(statement).all()
        return reports


def get_reports_by_terrorist(terrorist_id: int, limit: Optional[int] = None):
    """READ - Get all reports about a specific terrorist"""
    engine = get_engine()
    with Session(engine) as session:
        statement = select(Report).where(Report.terrorist_id == terrorist_id)
        if limit:
            statement = statement.limit(limit)
        reports = session.exec(statement).all()
        return reports


def search_reports_by_content(keyword: str):
    """READ - Search reports by keyword in content"""
    engine = get_engine()
    with Session(engine) as session:
        statement = select(Report).where(col(Report.content).contains(keyword))
        reports = session.exec(statement).all()
        return reports


def delete_report(report_id: int) -> bool:
    """DELETE - Remove a report from the database"""
    engine = get_engine()
    with Session(engine) as session:
        report = session.get(Report, report_id)
        if not report:
            print(f"\n❌ Report with ID {report_id} not found")
            return False
        
        session.delete(report)
        session.commit()
        print(f"✓ Report {report_id} deleted successfully")
        return True


def count_reports_by_terrorist(terrorist_id: int) -> int:
    """Count how many reports exist for a specific terrorist"""
    engine = get_engine()
    with Session(engine) as session:
        statement = select(func.count(col(Report.id))).where(col(Report.terrorist_id) == terrorist_id)
        count = session.exec(statement).one()
        return count


def get_dangerous_terrorists(min_reports: int = 5):
    """Find terrorists with more than min_reports reports (dangerous terrorists)"""
    engine = get_engine()
    with Session(engine) as session:
        # Get terrorists with report count
        statement = (
            select(Terrorist, func.count(col(Report.id)).label("report_count"))
            .join(Report, col(Terrorist.id) == col(Report.terrorist_id))
            .group_by(col(Terrorist.id))
            .having(func.count(col(Report.id)) > min_reports)
        )
        results = session.exec(statement).all()
        return results


def get_super_dangerous_terrorists():
    """Find super dangerous terrorists: >10 reports AND containing weapon keywords"""
    engine = get_engine()
    with Session(engine) as session:
        dangerous_keywords = ["פיגוע", "סכין", "רובה", "אקדח", "פצצה"]
        
        # First, get terrorists with more than 10 reports
        statement = (
            select(col(Terrorist.id), func.count(col(Report.id)).label("report_count"))
            .join(Report, col(Terrorist.id) == col(Report.terrorist_id))
            .group_by(col(Terrorist.id))
            .having(func.count(col(Report.id)) > 10)
        )
        
        potential_terrorists = session.exec(statement).all()
        
        super_dangerous = []
        for terrorist_id, report_count in potential_terrorists:
            # Check if any of their reports contain dangerous keywords
            if terrorist_id is None:
                continue
            
            terrorist = session.get(Terrorist, terrorist_id)
            if not terrorist:
                continue
                
            # Get all reports for this terrorist
            reports = get_reports_by_terrorist(terrorist_id)
            
            # Check if any report contains any of the keywords
            has_dangerous_content = False
            for report in reports:
                content_lower = report.content.lower()
                if any(keyword in content_lower for keyword in dangerous_keywords):
                    has_dangerous_content = True
                    break
            
            if has_dangerous_content:
                super_dangerous.append((terrorist, report_count))
        
        return super_dangerous
