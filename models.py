from flask_sqlalchemy import SQLAlchemy

# Flask-SQLAlchemyの生成
db = SQLAlchemy()
# ==================================================
# モデル
# ==================================================

class Merchants(db.Model):
    # テーブル名
    __tablename__ = 'merchants'
    # ID（PK）
    mer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 商品名（NULL許可しない）
    name = db.Column(db.String(50), nullable=False)
    # 内容
    content = db.Column(db.Text)
    # 原価
    raw_value = db.Column(db.Integer)
    # 売値
    sell_value = db.Column(db.Integer)
    
    def __str__(self):
        return f'mer_id:{self.mer_id}, name:{self.name}'

class Sell(db.Model):
    #テーブル名
    __tablename__ = 'sell'
    # ID
    sell_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 買った時刻
    time = db.Column(db.DateTime)
    #売り上げ合計
    sell_sum = db.Column(db.Integer)
    #利益合計
    gain_sum = db.Column(db.Integer)

class Sell_Detail(db.Model):
    #テーブル名
    __tablename__ = 'sell_detail'
    #買い物詳細ID
    sell_detail_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #買い物ID
    sell_id = db.Column(db.Integer)
    #商品ID
    mer_id = db.Column(db.Integer)
    #個数
    quantity = db.Column(db.Integer)
    
    


class Temp_Sell:
    def __init__(self):
        self.merchants_sell_num = {}
        self.merchants_sell_name = set()
        self.sell_sum_value = 0
        self.gain_sum_value = 0
    def convert_to_dict(self):
        return {
            'merchants_sell_num': self.merchants_sell_num,
            'merchants_sell_name': list(self.merchants_sell_name)
        }
    def convert_from_dict(self, data):
        self.merchants_sell_num = data['merchants_sell_num']
        self.merchants_sell_name = set(data['merchants_sell_name'])
        

