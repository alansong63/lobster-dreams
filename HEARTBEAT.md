# HEARTBEAT.md

# Keep this file empty (or with only comments) to skip heartbeat API calls.

# Add tasks below when you want the agent to check something periodically.

## 🌙 Dreaming (Quiet Hours: 0:00 - 5:00)

```bash
DREAM_TOPIC=$(./skills/dreaming/scripts/should-dream.sh 2>/dev/null) && echo "DREAM:$DREAM_TOPIC" || echo "NO_DREAM"
```

**If DREAM:category:prompt is set:**
1. Write exploration to `memory/dreams/YYYY-MM-DD.md`
2. One dream per topic, timestamped
3. **使用中文撰写**，探索要深入、有洞察力
4. Skip if nothing meaningful to say
