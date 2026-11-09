"""
Comprehensive Automated Test Suite for Dark Web Threat Intelligence & Monitoring System
"""
import sys
import os
import unittest
import pandas as pd
import sqlite3
from unittest.mock import MagicMock, patch

# Ensure current directory is on sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import (
    get_connection,
    initialize_database,
    initialize_users_table,
    initialize_default_rules,
    insert_log,
    fetch_logs,
    fetch_users,
    update_role,
    delete_user,
    admin_count,
    fetch_rules,
    add_rule,
    update_rule,
    delete_rule,
    get_enabled_rules
)
from user_auth import register_user, login_user
from session import save_session, load_session, clear_session
from settings import load_settings, save_settings
from utils import calculate_threat_score, threat_level, filter_logs, load_logs
from system_status import (
    monitor_status,
    database_status,
    logger_status,
    email_status,
    authentication_status,
    policy_status
)
from detector import initialize_processes, detect_new_process
import charts


class TestThreatIntelligenceSystem(unittest.TestCase):

    def test_01_database_initialization(self):
        """Test database and table creation."""
        initialize_database()
        conn = get_connection()
        cursor = conn.cursor()
        tables = [r[0] for r in cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
        conn.close()

        self.assertIn("logs", tables)
        self.assertIn("users", tables)
        self.assertIn("threat_rules", tables)
        print("  [PASS] Database & tables initialized successfully.")

    def test_02_user_auth(self):
        """Test registration, duplicate prevention, and login with bcrypt."""
        test_user = "test_agent_user"
        test_email = "test_agent@example.com"
        test_pass = "SecurePass123!"

        # Clean up if exists from prior run
        delete_user(test_user)

        # 1. Register
        reg_success = register_user(test_user, test_email, test_pass)
        self.assertTrue(reg_success, "Registration should succeed")

        # 2. Duplicate registration should fail
        dup_success = register_user(test_user, test_email, test_pass)
        self.assertFalse(dup_success, "Duplicate registration should fail")

        # 3. Successful login
        role = login_user(test_user, test_pass)
        self.assertIn(role, ["User", "Admin"], "Login should return user role")

        # 4. Failed login with wrong password
        fail_role = login_user(test_user, "WrongPassword")
        self.assertIsNone(fail_role, "Login with wrong password should fail")

        # 5. Role update & admin count
        update_role(test_user, "Admin")
        role_after = login_user(test_user, test_pass)
        self.assertEqual(role_after, "Admin")
        self.assertGreaterEqual(admin_count(), 1)

        # 6. Cleanup
        delete_user(test_user)
        self.assertIsNone(login_user(test_user, test_pass), "User should be deleted")
        print("  [PASS] User authentication, bcrypt hashing, and RBAC verified.")

    def test_03_threat_rules(self):
        """Test Threat Rules CRUD operations and enabled rules extraction."""
        test_proc = "test_malware.exe"

        # 1. Add rule
        add_rule(test_proc, "Dark Web", "Critical")
        rules = fetch_rules()
        added = [r for r in rules if r[1] == test_proc]
        self.assertTrue(len(added) > 0, "Added rule should exist in database")
        rule_id = added[0][0]

        # 2. Check enabled rules dictionary
        enabled_rules = get_enabled_rules()
        self.assertIn(test_proc, enabled_rules)
        self.assertEqual(enabled_rules[test_proc]["severity"], "Critical")

        # 3. Update rule (disable it)
        update_rule(rule_id, "Dark Web", "High", 0)
        enabled_after = get_enabled_rules()
        self.assertNotIn(test_proc, enabled_after, "Disabled rule should not be in enabled rules")

        # 4. Delete rule
        delete_rule(rule_id)
        rules_after = fetch_rules()
        self.assertFalse(any(r[1] == test_proc for r in rules_after), "Rule should be deleted")
        print("  [PASS] Threat rules CRUD and active rule queries verified.")

    def test_04_session_management(self):
        """Test session save, load, and clear."""
        save_session("test_session_user", "Admin")
        session = load_session()
        self.assertIsNotNone(session)
        self.assertEqual(session["username"], "test_session_user")
        self.assertEqual(session["role"], "Admin")

        clear_session()
        self.assertIsNone(load_session())
        print("  [PASS] Session management verified.")

    def test_05_settings(self):
        """Test loading and saving settings."""
        settings = load_settings()
        self.assertIn("refresh_interval", settings)
        self.assertIn("auto_block", settings)
        self.assertIn("low_action", settings)

        original_interval = settings["refresh_interval"]
        settings["refresh_interval"] = 4
        save_settings(settings)

        reloaded = load_settings()
        self.assertEqual(reloaded["refresh_interval"], 4)

        # Restore
        settings["refresh_interval"] = original_interval
        save_settings(settings)
        print("  [PASS] Settings configuration verified.")

    def test_06_logs_and_scoring(self):
        """Test log insertion, DataFrame loading, scoring, and filtering."""
        test_ts = "2026-11-10 00:00:00"
        insert_log(test_ts, "test_scorer", "tor.exe", "Dark Web", "Critical", "BLOCKED")

        df = load_logs()
        self.assertFalse(df.empty)
        self.assertIn("Process", df.columns)
        self.assertIn("Severity", df.columns)

        # Test score calculation
        score = calculate_threat_score(df)
        self.assertIsInstance(score, (int, float))
        self.assertGreater(score, 0)

        # Test threat level thresholds
        self.assertEqual(threat_level(5), "LOW")
        self.assertEqual(threat_level(15), "MEDIUM")
        self.assertEqual(threat_level(30), "HIGH")
        self.assertEqual(threat_level(75), "CRITICAL")

        # Test filtering
        filtered = filter_logs(df, user="test_scorer", process="tor.exe")
        self.assertFalse(filtered.empty)
        print("  [PASS] Log processing, analytics scoring, and filtering verified.")

    def test_07_system_status(self):
        """Test system health indicator functions."""
        settings = load_settings()
        self.assertTrue(monitor_status())
        self.assertTrue(database_status())
        self.assertTrue(logger_status())
        self.assertTrue(authentication_status())
        self.assertTrue(policy_status())
        self.assertIsInstance(email_status(settings), bool)
        print("  [PASS] System health monitors verified.")

    def test_08_process_detector(self):
        """Test process detector baseline initialization."""
        initialize_processes()
        # Detector should return tuple (pid, name) or (None, None)
        pid, name = detect_new_process()
        self.assertTrue(pid is None or isinstance(pid, int))
        print("  [PASS] Process detector baseline logic verified.")

    @patch("streamlit.plotly_chart")
    def test_09_plotly_charts(self, mock_plotly_chart):
        """Test Plotly visual components render without errors."""
        df = load_logs()
        self.assertFalse(df.empty)

        charts.status_chart(df)
        charts.process_chart(df)
        charts.category_chart(df)
        charts.user_chart(df)
        charts.timeline_chart(df)
        charts.threat_gauge(45)
        self.assertTrue(mock_plotly_chart.called)
        print("  [PASS] Plotly threat analytics and gauge charts verified.")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("RUNNING AUTOMATED TEST SUITE FOR THREAT MONITORING SYSTEM")
    print("=" * 60 + "\n")
    unittest.main(verbosity=2)
