# 🚀 Deploy RightsGuard to Brev.dev

## Prerequisites
1. Brev CLI installed: `pip install brev`
2. Brev account: https://console.brev.dev/signup
3. NVIDIA API key from hackathon

## Deployment Steps

### 1. Login to Brev
```bash
brev login
```

### 2. Create GPU instance
```bash
# From the RightsGuard directory
brev create rightsguard-demo
```

### 3. Set environment variables
When prompted, enter your NVIDIA_API_KEY

### 4. Access your app
After deployment, Brev will provide a URL like:
```
https://rightsguard-demo-[unique-id].brev.dev
```

## What Brev.dev Provides
- ✅ NVIDIA GPU instance (A100/V100)
- ✅ Public HTTPS URL
- ✅ Auto-restart on crashes
- ✅ 24/7 availability
- ✅ GPU acceleration for NeMo

## Demo Talking Points
"We deployed RightsGuard on Brev.dev's GPU infrastructure to leverage:
- NVIDIA GPU acceleration for faster inference
- Production-ready deployment with auto-scaling
- Public accessibility for community use
- Integration with the full NVIDIA AI ecosystem"

## Troubleshooting
- If deployment fails, check logs: `brev logs rightsguard-demo`
- Ensure all files are committed to git
- Verify NVIDIA_API_KEY is set correctly

## Cost Note
Brev.dev typically offers free credits for hackathons. Check your account dashboard.