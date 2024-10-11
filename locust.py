from locust import HttpUser, task, between
import os

class FastAPITestUser(HttpUser):
    wait_time = between(1, 3)  # 각 요청 사이의 대기 시간 (1~3초)

    @task
    def predict(self):
        # 테스트 이미지 경로
        image_path = os.path.join(os.path.dirname(__file__), "test_image.jpeg")
        
        # 파일 업로드를 위한 multipart 데이터 형식으로 파일 읽기
        with open(image_path, "rb") as image_file:
            files = {"file": ("test_image.jpeg", image_file, "image/jpeg")}
            # /predict 엔드포인트로 POST 요청
            self.client.post("/predict/", files=files)
