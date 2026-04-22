import pytest
from engagement import EngagementEngine

def test_initialization():
    engine = EngagementEngine("test_user")
    assert engine.user_handle == "test_user"
    assert engine.score == 0.0
    assert engine.verified is False

def test_process_interaction_weights():
    engine = EngagementEngine("test_user")
    engine.process_interaction("like", 1)    # 1 point
    engine.process_interaction("comment", 1) # 5 points
    engine.process_interaction("share", 1)   # 10 points
    assert engine.score == 16.0

def test_verified_multiplier():
    engine = EngagementEngine("pro_user", verified=True)
    engine.process_interaction("share", 1)
    # 10 * 1.5 = 15.0
    assert engine.score == 15.0

def test_invalid_interaction():
    engine = EngagementEngine("test_user")
    assert engine.process_interaction("follow") is False
    with pytest.raises(ValueError, match="Negative count"):
        engine.process_interaction("like", -1)

def test_tier_logic():
    engine = EngagementEngine("test_user")
    assert engine.get_tier() == "Newbie"
    
    engine.score = 100
    assert engine.get_tier() == "Influencer"
    
    engine.score = 1000
    assert engine.get_tier() == "Influencer"
    
    engine.score = 1001
    assert engine.get_tier() == "Icon"

def test_penalty_and_unverify():
    engine = EngagementEngine("risky_user", verified = True)
    engine.score = 100.0
    
    # Penalty with < 10 reports
    engine.apply_penalty(2) 
    # reduction = 100 * (0.20 * 2) = 40.0
    assert engine.score == 60.0
    assert engine.verified is True
    
    # Penalty with > 10 reports triggers unverify
    engine.apply_penalty(11)
    assert engine.verified is False
    assert engine.score == 0 # 60 * (0.2 * 11) = 132 reduction