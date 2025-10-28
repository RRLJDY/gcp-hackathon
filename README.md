# gcp-hackathon

# IoT AI Agent Service

IoT 환경을 위한 지능형 AI 에이전트 서비스로, 사물 인터넷 기기에서 수집된 정보를 기반으로 사용자에게 개인화되고 유용한 제안 및 경고를 제공합니다.

## 🚀 주요 기능

- **Vision-Language Model (VLM) 기반 영상 분석**: Google Gemini 2.5 Flash를 사용한 IoT 카메라 영상 실시간 분석 및 의미 있는 태그와 캡션 생성
- **계층형 멀티 에이전트 시스템**: ReAct 패턴을 사용하는 오케스트레이션 에이전트와 전문 하위 에이전트들
- **벡터 데이터베이스 기반 사용자 컨텍스트**: 의미 기반 검색을 통한 개인화된 서비스 제공
- **실시간 이미지 생성**: 알림에 맞는 컨텍스트 이미지 자동 생성
- **다중 플랫폼 알림**: FCM, APNS를 통한 푸시 알림 전송
- **학습 및 개선**: 사용자 피드백을 통한 지속적인 시스템 개선

## 🏗️ 아키텍처

### 5단계 에이전트 파이프라인

1. **인식 (Perception)**: IoT 기기에서 원시 데이터 수신
2. **분석 (Analysis)**: VLM을 통한 구조화된 정보 변환
3. **대기 (Queuing)**: 메시지 큐를 통한 비동기 처리
4. **추론 (Reasoning)**: AI 에이전트 스웜을 통한 상황 추론 및 행동 결정
5. **전달 (Delivery)**: 텍스트 제안과 이미지 생성 후 알림 전송

### 핵심 컴포넌트

- **VLMAnalyzer**: Google Gemini 2.5 Flash 기반 영상/이미지 분석
- **ContextAgent**: ReAct 패턴 기반 중앙 오케스트레이션 에이전트
- **SubAgents**: 반려동물, 택배, 보안 전문 에이전트들
- **UserContextService**: 벡터 데이터베이스 기반 사용자 컨텍스트 관리
- **ImageGenerationAgent**: 컨텍스트 기반 이미지 생성
- **NotificationService**: 다중 플랫폼 알림 전송

## 📋 요구사항

### 시스템 요구사항
- Python 3.8+
- Google Cloud Platform 계정
- Redis 서버
- 충분한 메모리 (최소 8GB 권장)

### API 키 및 서비스
- OpenAI API 키
- Google Cloud API 키
- Firebase 프로젝트 (FCM용)
- Apple Developer 계정 (APNS용, 선택사항)

## 🛠️ 설치 및 설정

### 1. 저장소 클론
```bash
git clone <repository-url>
cd gcp-hackathon
```

### 2. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate  # Windows
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

### 4. 환경 변수 설정
```bash
cp config.env.example .env
# .env 파일을 편집하여 API 키와 설정값 입력
```

### 5. Google Cloud 설정
```bash
# Google Cloud CLI 설치 및 인증
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# 필요한 API 활성화
gcloud services enable storage.googleapis.com
gcloud services enable pubsub.googleapis.com
gcloud services enable firestore.googleapis.com
```

### 6. Redis 서버 시작
```bash
redis-server
```

### 7. Celery 워커 시작
```bash
celery -A src.perception.event_processor worker --loglevel=info
```

## 🚀 사용법

### API 서버 시작
```bash
python api_server.py
```

### 데모 시나리오 실행
```bash
python examples/demo_scenarios.py
```

### 테스트 실행
```bash
pytest tests/ -v
```

## 📖 API 문서

서버 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 주요 엔드포인트

- `POST /events/process`: IoT 이벤트 처리
- `POST /events/upload`: 파일 업로드 및 이벤트 처리
- `POST /users/preferences`: 사용자 선호도 저장
- `POST /users/feedback`: 사용자 피드백 저장
- `GET /users/{user_id}/context`: 사용자 컨텍스트 조회
- `POST /notifications/send`: 알림 전송

## 🎯 사용 시나리오

### 1. 반려동물 모니터링
```python
# 반려견의 분리불안 증세 감지
event_data = {
    "device_id": "cam-livingroom-01",
    "device_type": "camera",
    "user_id": "user-001",
    "video_url": "path/to/video.mp4"
}

response = await process_event(event_data)
# 결과: "맥스가 불안해하고 있어요. 잠시 카메라를 확인해보시거나 목소리를 들려주세요."
```

### 2. 택배 배송 알림
```python
# 택배 도착 감지
event_data = {
    "device_id": "cam-frontdoor-01",
    "device_type": "camera", 
    "user_id": "user-001",
    "image_url": "path/to/image.jpg"
}

response = await process_event(event_data)
# 결과: "택배가 도착했습니다! 현관 앞에 안전하게 배치되었어요."
```

### 3. 보안 경고
```python
# 의심스러운 활동 감지
event_data = {
    "device_id": "cam-backyard-01",
    "device_type": "camera",
    "user_id": "user-001", 
    "video_url": "path/to/security_video.mp4"
}

response = await process_event(event_data)
# 결과: "의심스러운 활동이 감지되었습니다. 즉시 확인해주세요."
```

## 🔧 설정

### VLM 설정
```python
# src/config/settings.py
VLM_MODEL = "gpt-4-vision-preview"
VLM_MAX_TOKENS = 4096
VLM_TEMPERATURE = 0.1
```

### 에이전트 설정
```python
MAX_REACT_ITERATIONS = 10
CONTEXT_SEARCH_LIMIT = 5
IMAGE_GENERATION_TIMEOUT = 30
```

### 알림 설정
```python
FCM_SERVER_KEY = "your-fcm-server-key"
APNS_CERT_PATH = "path/to/apns/cert.pem"
```

## 📊 모니터링 및 로깅

### 로그 확인
```bash
# 애플리케이션 로그
tail -f logs/iot_agent.log

# 에러 로그
tail -f logs/iot_agent_error.log
```

### 메트릭 수집
- Prometheus 메트릭 지원
- 구조화된 JSON 로깅
- 실시간 성능 모니터링

## 🧪 테스트

### 단위 테스트
```bash
pytest tests/test_iot_agent.py -v
```

### 통합 테스트
```bash
pytest tests/test_integration.py -v
```

### 시나리오 테스트
```bash
python examples/demo_scenarios.py
```

## 🚀 배포

### Docker 배포
```bash
# Docker 이미지 빌드
docker build -t iot-ai-agent .

# 컨테이너 실행
docker run -p 8000:8000 iot-ai-agent
```

### Google Cloud Run 배포
```bash
# 이미지 빌드 및 푸시
gcloud builds submit --tag gcr.io/PROJECT_ID/iot-ai-agent

# Cloud Run에 배포
gcloud run deploy iot-ai-agent --image gcr.io/PROJECT_ID/iot-ai-agent --platform managed
```

### Kubernetes 배포
```bash
# Kubernetes 매니페스트 적용
kubectl apply -f k8s/
```

## 🤝 기여

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 📞 지원

- 이슈 리포트: [GitHub Issues](https://github.com/your-repo/issues)
- 문서: [Wiki](https://github.com/your-repo/wiki)
- 이메일: support@example.com

## 🙏 감사의 말

- Google의 Gemini 2.5 Flash 모델
- Google Cloud Platform
- LangChain 프레임워크
- FastAPI 프레임워크
- 모든 오픈소스 기여자들
