from dataclasses import dataclass

# dataclass 설명
# https://docs.python.org/ko/3/library/dataclasses.html


@dataclass
class ReviewData:
    review_text: str = ""
    kakao_map_name: str = ""
    blog_review_qty: str = ""
    star_review_stars: str = ""
    star_review_qty: str = ""
    # defualtValue: str = "defaultValue"
    # defualtList: list = field(init=False, default_factory=list) # init = False -> 초기화시 생성 불가
    # postInitValue: str

    # 초기화 함수
    # java Constructor 와 유사
    # https://stackoverflow.com/questions/23324731/correlation-between-constructors-in-java-and-init-function-in-python
    def __init__(self, review_text, kakao_map_name, blog_review_qty, star_review_stars, star_review_qty):
        self.review_text = review_text
        self.kakao_map_name = kakao_map_name
        self.blog_review_qty = blog_review_qty
        self.star_review_stars = star_review_stars
        self.star_review_qty = star_review_qty

    # 초기화 이후 동작
    # def __post_init__(self) -> None:
    #     self.postInitValue = f"{self.review_text} - {self.kakao_map_name}"
