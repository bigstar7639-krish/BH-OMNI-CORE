
from typing import Dict, List

class IntegrationError(Exception):
    pass

class AppOrchestrator:
    """
    Phase 4 Step 1 - Integration Orchestrator
    - Connects Core + Systems F-J into one flow
    - Flow: register feature -> create story -> synthesize voice -> list in marketplace
    - Uses real modules: FeatureRegistry, StoryEngine, VoiceEngine, Marketplace
    - No new business logic - Only wiring + validation
    - Any sub-module FAIL -> Whole flow FAIL (no silent partial success)
    """
    def __init__(self, registry, story_engine, voice_engine, marketplace):
        if registry is None or story_engine is None or voice_engine is None or marketplace is None:
            raise IntegrationError("All 4 modules required: registry, story, voice, marketplace")
        self.registry = registry
        self.story = story_engine
        self.voice = voice_engine
        self.market = marketplace
        self._flows = 0

    def publish_story_with_voice(self, story_title: str, genre: str, chapter_title: str, chapter_content: str, voice: str, seller: str, price_coins: int) -> dict:
        # Step 1 - Validate all inputs upfront (fail-fast)
        if not story_title or not isinstance(story_title, str):
            raise IntegrationError("story_title required")
        if not chapter_content or not isinstance(chapter_content, str):
            raise IntegrationError("chapter_content required")
        if price_coins is None or not isinstance(price_coins, int) or price_coins < 0:
            raise IntegrationError("price_coins must be >=0 int")
        # Step 2 - Register feature (Core)
        feature_id = f"F-{100 + self._flows + 1:03d}"
        try:
            self.registry.register(feature_id, f"Story: {story_title}", "story", "integration")
        except Exception as e:
            raise IntegrationError(f"Registry failed: {e}") from e
        # Step 3 - Create story (System F)
        try:
            self.story.create(story_title, genre)
            self.story.add_chapter(story_title, chapter_title, chapter_content)
        except Exception as e:
            raise IntegrationError(f"Story failed: {e}") from e
        # Step 4 - Synthesize voice preview (System F)
        try:
            voice_meta = self.voice.synthesize(chapter_content[:500], voice=voice)
        except Exception as e:
            raise IntegrationError(f"Voice failed: {e}") from e
        # Step 5 - List in marketplace (System J) - item_id from story title slug
        item_id = story_title.lower().replace(" ", "-")[:50]
        try:
            self.market.list_item(item_id, story_title, price_coins, seller, "story")
        except Exception as e:
            raise IntegrationError(f"Marketplace failed: {e}") from e
        self._flows += 1
        return {"flow": self._flows, "feature_id": feature_id, "story": story_title, "voice_duration_sec": voice_meta["duration_sec"], "market_item": item_id, "price_coins": price_coins, "status": "published"}

    def flow_count(self) -> int:
        return self._flows

    def get_info(self) -> dict:
        return {"flows_completed": self._flows, "principle": "Wiring only - Sub-module FAIL = Whole flow FAIL"}
