from dataclasses import dataclass

# dataclass 설명
# https://docs.python.org/ko/3/library/dataclasses.html


@dataclass
class ReviewData:
    review_text: str
    kakao_map_name: str
    blog_review_qty: str
    star_review_stars: str
    star_review_qty: str
    # defualtValue: str = "defaultValue"
    # defualtList: list = field(init=False, default_factory=list) # init = False -> 초기화시 생성 불가
    # postInitValue: str

    # 초기화 이후 동작
    # def __post_init__(self) -> None:
    #     self.postInitValue = f"{self.review_text} - {self.kakao_map_name}"
