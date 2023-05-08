from locust import HttpUser, task


class StressUser(HttpUser):
    @task
    def list_users(self):
        self.client.get("/api/v1/users")
