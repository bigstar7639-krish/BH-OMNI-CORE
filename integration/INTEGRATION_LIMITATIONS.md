# Integration Limitations

## Phase 4 Step 1 - App Orchestrator
- Wiring only - No new business logic
- Uses real modules: FeatureRegistry, StoryEngine, VoiceEngine, Marketplace
- Limitations: In-memory, no auth in this flow (Phase 1 auth separate), no real TTS audio
- DO NOT CLAIM full app - This is integration wiring only
- PHASE 4: Integration - Step 1

## Step 2 - Secure Gateway
- Wires PermissionManager + SecureAPIGateway
- Limitations: No JWT validation in this wiring (sessions separate), no rate limiting here
- DO NOT CLAIM full auth - This is permission + gateway wiring only
