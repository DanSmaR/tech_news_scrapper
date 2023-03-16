import pytest
from unittest.mock import patch
from tech_news.analyzer.reading_plan import (
    ReadingPlanService,
)  # noqa: F401, E261, E501
from tests.assets.news import NEWS


EXPECTED_RESULT = {
    "time_available": 5,
    "result": {
        "readable": [
            {
                "unfilled_time": 1.0,
                "chosen_news": [
                    ("noticia_0", 2.0),
                    ("Notícia bacana 2", 1.0),
                    ("noticia_3", 1.0),
                ],
            },
            {"unfilled_time": 1.0, "chosen_news": [("Notícia bacana", 4.0)]},
            {
                "unfilled_time": 2.0,
                "chosen_news": [
                    ("noticia_4", 1.0),
                    ("noticia_5", 1.0),
                    ("noticia_6", 1.0),
                ],
            },
            {"unfilled_time": 0.0, "chosen_news": [("noticia_9", 5.0)]},
        ],
        "unreadable": [("noticia_7", 7.0), ("noticia_8", 8.0)],
    },
}


@patch(
    "tech_news.analyzer.reading_plan.ReadingPlanService._db_news_proxy"
)
def test_reading_plan_group_news(mock_find_news):
    # Testar entrada com valor inválido
    with pytest.raises(
        ValueError, match="Valor 'available_time' deve ser maior que zero"
    ):
        ReadingPlanService.group_news_for_available_time(0)

    # Testar valores 'unfilled_time' inconsistentes
    mock_find_news.return_value = NEWS
    result = ReadingPlanService.group_news_for_available_time(5)
    for index, group in enumerate(result["readable"]):
        assert (
            group["unfilled_time"]
            == EXPECTED_RESULT["result"]["readable"][index]["unfilled_time"]
        )

    # Testar valores em 'readable
    assert result["readable"] == EXPECTED_RESULT["result"]["readable"]

    # Testar valores em 'unreadable
    assert result["unreadable"] == EXPECTED_RESULT["result"]["unreadable"]
