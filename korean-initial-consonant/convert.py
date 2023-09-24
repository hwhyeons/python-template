import functools

"""
초성 검색
"""

d = [["ㄱ", ["가", "까"]], ["ㄲ", ["까", "나"]], ["ㄴ", ["나", "다"]], ["ㄷ", ["다", "따"]],
     ["ㄸ", ["따", "라"]], ["ㄹ", ["라", "마"]], ["ㅁ", ["마", "바"]], ["ㅂ", ["바", "빠"]],
     ["ㅃ", ["빠", "사"]], ["ㅅ", ["사", "싸"]], ["ㅆ", ["싸", "아"]], ["ㅇ", ["아", "자"]], ["ㅈ", ["자", "짜"]],
     ["ㅉ", ["짜", "차"]], ["ㅊ", ["차", "카"]], ["ㅋ", ["카", "타"]], ["ㅌ", ["타", "파"]], ["ㅍ", ["파", "하"]],
     ["ㅎ", ["하", "힣"]]]

@functools.cache
def convert2initial_constant(s):
    """
    초성으로 변환
    :param s:
    :return:
    """
    global d
    ans = ''
    for ch in s:
        ch_ord = ord(ch)
        flag=False
        for all in d:
            ord1 = ord(all[1][0])
            ord2 = ord(all[1][1])
            if ord1 <= ch_ord < ord2:
                ans+=all[0]
                flag=True
                break
        if not flag:
            ans+=ch # 한글이 아니면 원본 글자 추가
    return ans

@functools.cache
def find_with_initial_constant(find: str,full: str):
    """
    초성이 있는지 검색
    :return:
    """
    find_initial = convert2initial_constant(find)
    full_initial = convert2initial_constant(full)
    return full_initial.index(find_initial)
    

if __name__ == '__main__':
    s = '테스트'
    print(convert2initial_constant(s))
    print(find_with_initial_constant('ㄱㄴ다','마바사가나다라'))
