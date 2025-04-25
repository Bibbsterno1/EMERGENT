import requests
import pytest
from datetime import datetime

class TestHubSpotQuirkyNewsAPI:
    def __init__(self):
        # Get backend URL from frontend .env
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    self.base_url = line.split('=')[1].strip()
                    break
        
        if not self.base_url:
            raise Exception("Could not find REACT_APP_BACKEND_URL in frontend/.env")

    def test_health_check(self):
        """Test the health check endpoint"""
        response = requests.get(f"{self.base_url}/api/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
        assert "timestamp" in data
        print("✅ Health check endpoint working")

    def test_company_info(self):
        """Test getting company information"""
        response = requests.get(f"{self.base_url}/api/company-info", params={"name": "Acme Corporation"})
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Acme Corporation"
        assert data["industry"] == "Technology"
        assert len(data["quirkNews"]) > 0
        print("✅ Company info endpoint working")

        # Test invalid company
        response = requests.get(f"{self.base_url}/api/company-info", params={"name": "Invalid Company"})
        assert response.status_code == 404
        print("✅ Company info 404 handling working")

    def test_companies_list(self):
        """Test getting all companies"""
        response = requests.get(f"{self.base_url}/api/companies")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        print("✅ Companies list endpoint working")

    def test_quirky_news(self):
        """Test getting quirky news for a company"""
        response = requests.get(f"{self.base_url}/api/quirky-news", params={"company_name": "Acme Corporation"})
        assert response.status_code == 200
        data = response.json()
        assert "news" in data
        assert isinstance(data["news"], list)
        assert len(data["news"]) > 0
        print("✅ Quirky news endpoint working")

        # Test company with no news
        response = requests.get(f"{self.base_url}/api/quirky-news", params={"company_name": "Unknown Company"})
        assert response.status_code == 200
        data = response.json()
        assert len(data["news"]) == 0
        print("✅ Quirky news empty response working")

    def test_hubspot_setup(self):
        """Test HubSpot setup endpoint"""
        response = requests.get(f"{self.base_url}/api/hubspot/setup")
        assert response.status_code == 200
        data = response.json()
        assert "isConfigured" in data
        assert "authUrl" in data
        print("✅ HubSpot setup endpoint working")

    def run_all_tests(self):
        """Run all API tests"""
        print("\n🔍 Starting API tests...")
        
        try:
            self.test_health_check()
            self.test_company_info()
            self.test_companies_list()
            self.test_quirky_news()
            self.test_hubspot_setup()
            print("\n✨ All API tests passed successfully!")
            
        except AssertionError as e:
            print(f"\n❌ Test failed: {str(e)}")
            raise
        except Exception as e:
            print(f"\n❌ Error during testing: {str(e)}")
            raise

if __name__ == "__main__":
    tester = TestHubSpotQuirkyNewsAPI()
    tester.run_all_tests()
