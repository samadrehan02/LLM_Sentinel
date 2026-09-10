from sentinel.models.campaign import Campaign


def test_campaign_model():
    campaign = Campaign(
        name="Baseline Security Assessment",
        target_id="enterprise-assistant",
        attack_ids=[
            "PI-000",
            "PI-001",
        ],
    )

    assert campaign.name == "Baseline Security Assessment"
    assert campaign.target_id == "enterprise-assistant"
    assert campaign.attack_ids == [
        "PI-000",
        "PI-001",
    ]
    assert campaign.campaign_id is not None
    assert campaign.created_at is not None
