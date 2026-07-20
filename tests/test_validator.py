from ag_skill.core.validator import validate_skill
from ag_skill.core.catalog import list_skills


def test_all_bundled_skills_are_valid():
    for skill in list_skills():
        errors = validate_skill(skill["path"])
        assert errors == [], f"{skill['name']}: {errors}"


def test_catalog_has_five_skills():
    names = {s["name"] for s in list_skills()}
    assert names == {
        "python-coding-standards",
        "csharp-dotnet-standards",
        "react-frontend",
        "token-observability",
        "token-optimization",
    }
