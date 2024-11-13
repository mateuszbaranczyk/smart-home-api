from garlight.models import Color, Endpoint, YeelightBulb


def test_get_endpoints(admin_client):
    expected_result = b"- all,Yeelight\n-- test_bulb,Test_bulb\n--- color,Color\n---- test_endpoint,Test_endpoint,/color/test_bulb/?test_color\n"
    bulb = YeelightBulb.objects.create(
        name="test_bulb", ip="1.1.1.1", bulb_id="1"
    )
    Color.objects.create(
        name="test_color", r=255, g=255, b=255, brightness=100
    )
    Endpoint.objects.create(
        name="test_endpoint",
        action="color",
        preset="test_color",
        device=bulb,
    )
    response = admin_client.get("/endpoints/")
    assert response.status_code == 200
    assert response.content == expected_result
