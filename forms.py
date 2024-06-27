from flask_wtf import FlaskForm
from wtforms import Form, StringField, IntegerField, TextAreaField, SubmitField, FieldList, FormField
from wtforms.validators import DataRequired, Length, ValidationError
from models import Merchants
max_merchants = 100

# ==================================================
# Formクラス
# ==================================================
# 商品用入力クラス
class MerchantForm(FlaskForm):
    # 商品名
    name = StringField('商品名：', validators=[DataRequired('商品名は必須入力です'), 
                            Length(max=20, message='20文字以下で入力してください')])
    # 内容
    content = TextAreaField('内容：')
    # 原価
    raw_value = StringField('原価：')
    #　売値
    sell_value = StringField('売値：')
    # ボタン
    submit = SubmitField('送信')

    # カスタムバリデータ
    def validate_title(self, name):
        # StringFieldオブジェクトではなく、その中のデータ（文字列）をクエリに渡す必要があるため
        # 以下のようにname.dataを使用して、StringFieldから実際の文字列データを取得する
        merchant = Merchants.query.filter_by(name=name.data).first()
        if merchant:
            raise ValidationError(f"商品名 '{name.data}' は既に存在します。\
                                  別の商品名を入力してください。")


class SubRegisterForm(Form):
    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False  # 子フォームではCSRFトークンが生成されないように設定
        super(SubRegisterForm, self).__init__(*args, **kwargs)
    
    def set_label(self, label_text):
        self.quantity.label = label_text
    
    def show_label(self):
        return self.quantity.label.text
    def show_data(self):
        return self.quantity.data

    quantity = IntegerField('Error!', validators=[DataRequired()], default=0)
    

class RegisterForm(FlaskForm):
    submit = SubmitField('会計へ')
    merchants = FieldList(FormField(SubRegisterForm))

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        #self.merchants = FieldList(FormField(SubmitField))
        #while len(self.merchants) > 0:
        #    self.merchants.pop_entry()
        
        #leng = len(self.merchants)
        all_merchants = Merchants.query.all()
        cnt = 0
        for merchant in all_merchants:
            # Append an empty SubRegisterForm
            self.merchants.append_entry()
            # Set the label for the quantity field
            self.merchants[cnt].quantity.label.text = merchant.name
            cnt += 1
        print('==========')
        #print(f'len(before):{leng}')
        print(f'cnt:{cnt}')
        print(f'len:{len(self.merchants)}')
        print('==========')
    """
    def show_first_label(self):
        merchant = self.merchants.pop_entry()
        self.merchants.append_entry(merchant)
        return merchant.show_label()
    def show_first_data(self):
        merchant = self.merchants.pop_entry()
        self.merchants.append_entry(merchant)
        return merchant.show_data()
    """


    #def __str__(self):
    #    return self.merchants.entries[-1].quantity.label.text

class CalculateForm(FlaskForm):
    in_money = IntegerField('お預かり')
    submit = SubmitField('会計')
    


"""
class RegisterForm(FlaskForm):
    submit = SubmitField('会計へ')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.merchants_sell_num = []
        for merchant in Merchants.query.all():
            field = IntegerField(f'{merchant.name}', validators=[DataRequired()])
            self.merchants_sell_num.append(field)
            self.__setattr__(f'merchant_{merchant.mer_id}', field)


class RegisterForm(FlaskForm):
    merchants_sell_num = [0] * max_merchants
    #num = IntegerField('how many')
    for merchant in Merchants.query.all():
        #nums = IntegerField(f'{merchant.name}')
        merchants_sell_num[merchant.mer_id] = IntegerField(f'{merchant.name}').data
    submit = SubmitField('会計へ')
"""


