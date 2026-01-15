from app import create_app, User
import unittest

class LoginTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        self.client = self.app.test_client()
        
        with self.app.app_context():
            # Ensure admin exists is handled by app startup or seed
            # We assume database is populated as per debug_login.py
            pass

    def test_admin_login(self):
        print("Testing Admin Login...")
        response = self.client.post('/login', data={
            'email': 'admin@university.com',
            'password': 'admin123'
        }, follow_redirects=True)
        
        print(f"Status Code: {response.status_code}")
        if response.history:
            print("Redirect History:")
            for resp in response.history:
                print(f" - {resp.status_code} : {resp.location}")
                
        # Check if we are on dashboard
        if b'Admin Dashboard' in response.data:
            print("SUCCESS: Logged in and reached Admin Dashboard")
        elif b'Login' in response.data:
            print("FAILURE: Still on Login page")
            # Print flashes if any
            if b'Login failed' in response.data:
                print("Flash: Login failed")
        else:
            print("UNKNOWN State")
            # print(response.data[:500]) # Print start of page

if __name__ == '__main__':
    unittest.main()
