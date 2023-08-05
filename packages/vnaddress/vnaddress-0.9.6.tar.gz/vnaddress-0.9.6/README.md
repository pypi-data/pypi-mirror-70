# Vietnamese address standardizer - Bộ chuẩn hóa  địa chỉ Việt Nam
A package for parsing Vietnamese address


## Tính năng
1. Xử lỹ những tên viết tắt thông dụng
2. Sửa chính tả
3. Sửa lỗi thứ tự tên đơn vị hành chính
4. Thêm prefix (xã, huyện, tỉnh, ...)


## Cài đặt qua PyPi
```shell
pip3 install vnaddress
```

## Thử nghiệm
```python

from vnaddress import VNAddressStandardizer

address = VNAddressStandardizer(raw_address = "Dicjh Vongj Haaju", comma_handle = True)
address.execute()

# output
# phường Dịch Vọng Hậu, quận Cầu Giấy, thành phố Hà Nội


address = VNAddressStandardizer(raw_address = "Dicjh Vongj Haaju, ", comma_handle = True, detail=True)
address.execute()

# output
# phường Dịch Vọng Hậu, quận Cầu Giấy, thành phố Hà Nội

```

#### 更新pypi仓库
```
cd python
python setup.py sdist bdist_wheel
python -m twine upload dist/*
```

### c++

clone到本地直接编译即可
```shell
cd text-clean
bazel build //:test
```

具体用法请参考[test.cc](./test.cc)

效果如下:
```text
转换前:繁 體 字是smasd ❶ ❷ ❸ ❹  彩呗我 幹什麼 □ ■ ◇ ◆ − + ⑪ ⑫ ⑬  ⒍ ⒎ ⒏ ⒐ W,X  asd鬼东 西錯 鍼٩(๑ᵒ̴̶͈᷄ᗨᵒ̴̶͈᷅)و q🕓🕛,
转换后:繁体字是smasd1234彩呗我干什么+1112136789wxasd鬼东西错针q

转换前:神谕23 速度来各种老手+——++++++来个大法师+++
转换后:神谕23速度来各种老手+++来个大法师+++
```
