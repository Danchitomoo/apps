from flask import render_template, request, redirect, url_for, flash, session
from app import app
from models import db, Merchants, Temp_Sell, Sell
from forms import MerchantForm, RegisterForm, CalculateForm
from function import db_update


# ==================================================
# ルーティング
# ==================================================

    
# 一覧
@app.route("/register/index/<change>")
def index(change):
    # メモ全件取得
    merchants = Merchants.query.all()
    # 画面遷移
    return render_template("index.html", merchants=merchants, change=change)

# 登録
@app.route("/register/create", methods=["GET", "POST"])
def create():
    # POST時
    #formインスタンス作成
    form = MerchantForm()
    if request.method == "POST":
        if form.validate_on_submit():
            # データ入力取得
            name = form.name.data
            content = form.name.data
            raw_value = form.raw_value.data
            sell_value = form.sell_value.data
            # 登録処理
            merchant = Merchants(name=name, content=content, raw_value=raw_value, sell_value=sell_value)
            db.session.add(merchant)
            db.session.commit()
            #flash message
            flash('登録しました')
            # 画面遷移
            return redirect(url_for("index", change=0))
    # GET時
    # 画面遷移
    return render_template("create_form.html", form=form)

# 更新
@app.route("/register/update/<int:mer_id>", methods=["GET", "POST"])
def update(mer_id):
    # データベースからmer_idに一致する商品を取得し、
    # 見つからない場合は404エラーを表示
    target_data = Merchants.query.get_or_404(mer_id)
    form = MerchantForm(obj=target_data)
    # POST時
    if request.method == "POST":
        # 変更処理
        target_data.name = form.name.data
        target_data.content = form.content.data
        target_data.raw_value = form.raw_value.data
        target_data.sell_value = form.sell_value.data
        db.session.commit()
        #flash message
        flash('変更しました')
        # 画面遷移
        return redirect(url_for("index", change=0))
    # GET時
    # 画面遷移
    return render_template("update_form.html", form=form, edit_id=target_data.mer_id)

# 削除
@app.route("/register/delete/<int:mer_id>")
def delete(mer_id):
    # データベースからmemo_idに一致するメモを取得し、
    # 見つからない場合は404エラーを表示
    merchant = Merchants.query.get_or_404(mer_id)
    # 削除処理
    db.session.delete(merchant)
    db.session.commit()
    # 画面遷移
    return redirect(url_for("index", change=0))

# 入力
@app.route("/register/input", methods=['GET', 'POST'])
def regi_input():
    #会計入力画面
    temp = Temp_Sell()
    form = RegisterForm()
    print(f'len:{len(form.merchants)}')
    if request.method == 'POST':
            sell_sum_value = 0
            gain_sum_value = 0
            for _ in range(len(form.merchants)):
                merchant_form = form.merchants.pop_entry()
                data_value = merchant_form.quantity.data
                if data_value > 0:
                    mer_label = merchant_form.show_label()
                    merchant = Merchants.query.filter_by(name=mer_label).first()
                    if merchant:
                        index = str(merchant.mer_id)
                        sell_value = merchant.sell_value
                        raw_value = merchant.raw_value
                        sell_sum_value += sell_value * merchant_form.quantity.data
                        gain_sum_value += (sell_value - raw_value) * merchant_form.quantity.data
                        temp.merchants_sell_num[index] = merchant_form.quantity.data
                        temp.merchants_sell_name.add(index)
            session['temp_sell_data'] = temp.convert_to_dict()
            session['sell_sum_value'] = sell_sum_value
            session['gain_sum_value'] = gain_sum_value
            return redirect(url_for('register'))
    # GET時
    merchants = Merchants.query.all()
    return render_template('regi_input_form.html', form=form, merchants=merchants)

#お釣り計算
@app.route("/register/register", methods=['GET', 'POST'])
def register():
    form = CalculateForm()
    if request.method == 'POST':
            in_money = form.in_money.data
            temp_sell_data = session.get('temp_sell_data')
            if temp_sell_data is None:
                return redirect(url_for('regi_input'))
            
            #print(temp_sell_data)
            temp = Temp_Sell()
            temp.convert_from_dict(temp_sell_data)
            temp.sell_sum_value = session['sell_sum_value']
            temp.gain_sum_value = session['gain_sum_value']
            if in_money >= temp.sell_sum_value:
                change = in_money - temp.sell_sum_value
                db_update(temp)
                return redirect(url_for('index', change=change))
            else:
                return render_template('register_form.html', form=form, error=True)
    else:
        return render_template('register_form.html', form=form)
            
#売り上げ表示
@app.route('/register/show/gain')
def show_gains():
    try:
        last_sell = db.session.query(Sell).order_by(Sell.sell_id.desc()).first()
        last_sell_sum = last_sell.sell_sum
        last_gain_sum = last_sell.gain_sum
    except:
        last_sell_sum = 0
        last_gain_sum = 0
    return render_template('show_gains.html', sell_sum=last_sell_sum, gain_sum = last_gain_sum)
    

# モジュールのインポート
from werkzeug.exceptions import NotFound

# エラーハンドリング
@app.errorhandler(NotFound)
def show_404_page(error):
    msg = error.description
    print('エラー内容：',msg)
    return render_template('errors/404.html', msg=msg) , 404


