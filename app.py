import glob
import json
import os
import random
from numpy import place
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore 
from firebase_admin import storage
import pyrebase
import requests
import toml

st.set_page_config(layout="wide",page_title="RENTURE")
hide_st_style = """<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}</style>"""

firebaseConfig = {
  "apiKey": "AIzaSyChVGq2Rcu4KkUfzcRblmrRdvHNoysvKKw",
  "authDomain": "renture-3fde0.firebaseapp.com",
  "projectId": "renture-3fde0",
  "storageBucket": "renture-3fde0.appspot.com",
  "messagingSenderId": "975601507437",
  "appId": "1:975601507437:web:ab07f146593ed72f25f364",
  "measurementId": "G-7R8LDS8FH3",
  "databaseURL": ""
}

firebase = pyrebase.initialize_app(firebaseConfig) 
cred = credentials.Certificate(dict(st.secrets))

if 'auth' not in st.session_state:
    st.session_state['auth'] = firebase.auth()
if 'user_details' not in st.session_state:
    st.session_state['user_details'] = st.session_state['auth'].current_user
if 'user_custom_details' not in st.session_state:
    st.session_state['user_custom_details'] = {}
if 'app_init' not in st.session_state:
    st.session_state['app_init'] = False
if 'Login_status' not in st.session_state:
    st.session_state['Login_status'] = 'Sign in'

try:
    if st.session_state['app_init'] == False:
        firebase_admin.initialize_app(cred)
        st.session_state['app_init'] = True
except:
    st.session_state['app_init'] = True

storage_py = firebase.storage()
db = firestore.client()
bucket = storage.bucket(firebaseConfig['storageBucket'])

def change_to_signup():
    st.session_state['Login_status'] = 'Sign up'

def change_to_signin():
    st.session_state['Login_status'] = 'Sign in'

def signup():
    def user_signup():
        if password!= Con_password:
            st.error('Password does not match')
            return
        if info_['User Name']=='' or address1=='' or address2=='' or pin_code=='' or city=='' or info_['Phone Number']=='':
            st.error('All fields are required')
            return
        try:
            st.session_state['auth'].create_user_with_email_and_password(st.session_state.email, st.session_state.password)
            st.success('Email created successfully')
            db.collection('Costumers').document(st.session_state.email).set(info_)
            st.session_state['Login_status'] = 'Sign in'
        except Exception as e:
            st.error(json.loads(e.args[1])['error']['message'].replace('_', ' '))

    si = st.columns([0.5,1,0.6,1,0.4])
    si[1].title('Sign Up')
    si[3].title('')
    si[3].title('')
    si[3].title('RENTURE')
    si[3].write('Online rental Platform')
    text_signup = st.columns([1,1,1,4])
    text_signup[1].write('Already have an account')
    text_signup[2].button('Sign in', on_click=change_to_signin)
    info_={}
    with si[1].container():
        info_['User Name'] = st.text_input('User Name',key = 'User Name', placeholder = 'User Name')
        st.text_input('Email',key = 'email', placeholder = 'Email')
        password = st.text_input('Password',key = 'password', placeholder = 'Password',type='password')
        Con_password = st.text_input('Confirm Password',key = 'Con_password', placeholder = 'Password',type='password')
        address1 = st.text_input('Address',key = 'Street address', placeholder = 'Street address')
        address2 = st.text_input('Address',key = 'Street address line 2', placeholder = 'Street address line 2')
        with open('city_state.json','r') as f:
            city__state= json.load(f)
        def get_api_address():
            try:
                response1 = requests.get(f'https://api.postalpincode.in/pincode/{st.session_state["Pin Code"]}')
                if response1.json()[0]['PostOffice'][0]['State'] in city__state.keys():
                    st.session_state['State'] = response1.json()[0]['PostOffice'][0]['State']
                    if response1.json()[0]['PostOffice'][0]['District'] in city__state[response1.json()[0]['PostOffice'][0]['State']]:
                        st.session_state['Distt'] = response1.json()[0]['PostOffice'][0]['District']
                st.session_state['city'] = response1.json()[0]['PostOffice'][0]['Block']
            except:
                st.error('Please enter a valid pin code')
        pin_code = st.text_input('Pin Code',key = 'Pin Code', placeholder = 'Pin code',on_change=get_api_address)
        state = st.selectbox('State',city__state.keys(),key = 'State',)
        distt = st.selectbox('District',city__state[state],key = 'Distt')
        city = st.text_input('City',placeholder='city',key = 'city')
        info_['Phone Number'] = st.text_input('Phone Number',key = 'Phone Number', placeholder = '+91')
        info_['Address'] = f'{address1}, {address2}, {city}, {distt}, {state}, {pin_code}'
        st.button('Sign up', on_click=user_signup)
            
def signin():
    def user_signin():
        try:
            res = st.session_state['auth'].sign_in_with_email_and_password(st.session_state.email_signin, st.session_state.password_signin)
            st.session_state['user_details'] = st.session_state['auth'].current_user
        except Exception as e: 
            st.error(json.loads(e.args[1])['error']['message'].replace('_', ' '))
    si = st.columns([0.5,1,0.6,1,0.4])
    si[1].title('Sign in')
    si[3].title('')
    si[3].title('')
    si[3].title('RENTURE')
    si[3].write('Online rental Platform')
    text_signup = st.columns([1,1,1,4])
    text_signup[1].write('Do not have an account')
    text_signup[2].button('Sign up', on_click=change_to_signup)
    with si[1].container():
        st.text_input('Email',key = 'email_signin', placeholder = 'Email')
        st.text_input('Password',key = 'password_signin', placeholder = 'Password',type='password')
        st.button('Sign in', on_click= user_signin)

if st.session_state['user_details'] == None:
    if st.session_state['Login_status'] == 'Sign in':
        signin()
    if st.session_state['Login_status'] == 'Sign up':
        signup()
    st.stop()

if len(st.session_state['user_custom_details']) == 0:
    st.session_state['user_custom_details'] = db.collection('Costumers').document(st.session_state['user_details']['email']).get().to_dict()
# # st.markdown(hide_st_style, unsafe_allow_html=True)
arr1 = st.columns([1,2,.2,.4,.25,.25])
arr1[0].title('RENTURE')
arr1[1].text_input('',placeholder='Search')
arr1[3].title('')
arr1[3].write(f'###### hello, {st.session_state["user_custom_details"]["User Name"]}')
arr1[4].title('')
arr1[4].write('###### Return')
arr1[5].title('')
arr1[5].write('###### Cart')

col=4
fill_star = '<img src="https://img.icons8.com/fluency/344/filled-star.png"  width="20" >'
half_star = '<img src="https://img.icons8.com/fluency/344/star-half.png" width="20">'
empty_star = '<img src="https://img.icons8.com/color/344/star--v1.png" width="20">'

rating_arr =[half_star+empty_star*4,
                fill_star+empty_star*4,
                fill_star+half_star+empty_star*3,
                fill_star*2+empty_star*3,
                fill_star*2+half_star+empty_star*2,
                fill_star*3+empty_star*2,
                fill_star*3+half_star+empty_star,
                fill_star*4+empty_star,
                fill_star*4+half_star,
                fill_star*5]

if 'state' not in st.session_state:
    st.session_state['state'] = 'home'

if 'curr_book' not in st.session_state:
    st.session_state['curr_book'] = ''

if 'chached_books' not in st.session_state:
    st.session_state['chached_books'] = []

def state_change(i,j):
    st.session_state['curr_book'] = st.session_state['chached_books'][(i*col+j)]
    st.session_state['state'] = 'rent'

def state_change_back():
    st.session_state['curr_book'] = ''
    st.session_state['state'] = 'home'

def state_change_seller():
    st.session_state['state'] = 'seller'

arr2 = st.columns([8.7,1.1])
if st.session_state['state'] == 'home':
    arr2[1].button('Rent/Sell books', on_click=state_change_seller)

if st.session_state['state'] == 'seller':
    arr2[1].button('Buy/Rent books', on_click=state_change_back)

if st.session_state['state'] == 'home':
    if len(st.session_state['chached_books']) == 0:
        books_arr=[]
        get_books = db.collection_group('Uploaded Books')
        docs = get_books.stream()
        for doc in docs:
            books_arr.append(doc.to_dict())
        st.session_state['chached_books'] = books_arr
    size=int(len(st.session_state['chached_books'])/col)
    st.header('Best sellers')
    st.subheader('')
    for i in range(size):
        arr=st.columns([1]*col)
        for j in range(col):
            arr[j].image(st.session_state['chached_books'][(i*col+j)]["book_location"][0],width=200)
            arr[j].markdown(f'''{arr[(i*col+j)]["Book name"]}<br>
            {random.choice(rating_arr)} {str(random.randint(500,5000))} <br>
            Rent Price:  <span style="color:green">₹{arr[(i*col+j)]["Rent price"]}</span>''',True)
            arr[j].button('Rent/Buy',key=str(i)+str(j),on_click=state_change,args=(i,j))
        st.title('')
    arr=st.columns([1]*col)
    for i in range(len(st.session_state['chached_books'])%col):
            arr[i].image(st.session_state['chached_books'][(size*col)+i]["book_location"][0],width=200)
            arr[i].markdown(f'''{st.session_state['chached_books'][(size*col)+i]["Book name"]}<br>
            {random.choice(rating_arr)} {str(random.randint(500,5000))} <br>
            Rent Price:  <span style="color:green">₹{st.session_state['chached_books'][(size*col)+i]["Rent price"]}</span>''',True)
            arr[i].button('Rent/Buy',key=str(i),on_click=state_change,args=(size,i))

if st.session_state['state'] == 'rent':
    arr=st.columns([1.5,3.7,1.2])
    arr[0].image(st.session_state['curr_book']["book_location"][0], width=250)
    arr[1].header(st.session_state['curr_book']["Book name"])
    arr[1].markdown(f'''by {st.session_state['curr_book']['Author name']}<br>
                        {random.choice(rating_arr)} {str(random.randint(500,5000))} <br>
                        Rent Price:  <span style="color:green">₹{st.session_state['curr_book']["Rent price"]}</span>''',True)
    with arr[1].container():
         buy_rent = option_menu(None,['Rent ₹'+st.session_state['curr_book']["Rent price"],'Buy ₹'+st.session_state['curr_book']['Sell price']],
                                     icons=['truck','bag-fill'], menu_icon="check2-circle", orientation="horizontal",
                            styles={"container": {"background-color": "#0d1017",
                             "width":"500px", "margin-left": "0", "padding-left":"0"}})
    
    arr[1].write(st.session_state['curr_book']['Description'][:500]+'....')

    with arr[2].form('buy'):
        st.write(buy_rent.split(' ')[0]+' price:',buy_rent.split(' ')[-1])
        st.write('Discount: -₹50')
        st.write('Shipping charges: ₹50')
        st.write('##### Total: '+buy_rent.split(' ')[-1])
        st.write('###### Estimated time: 2hrs')
        st.form_submit_button('Buy Now')
    arr[2].button('Continue Shopping',on_click=state_change_back)

    st.header('')
    st.write('---')

    st.header('Recommended Books')
    st.header('')
    for i in range(min(2,int(len(st.session_state['chached_books'])/col)+1)):
        arr=st.columns([1]*col)
        for j in range(min(col,len(st.session_state['chached_books'])-col*i)):
            arr[j].image(st.session_state['chached_books'][(i*col+j)]["book_location"][0],width=200)
            arr[j].markdown(f'''{st.session_state['chached_books'][(i*col+j)]["Book name"]}<br>
            {random.choice(rating_arr)} {str(random.randint(500,5000))} <br>
            Rent Price:  <span style="color:green">₹{st.session_state['chached_books'][(i*col+j)]["Rent price"]}</span>''',True)
            arr[j].button('Rent/Buy',key=str(i)+str(j),on_click=state_change,args=(i,j))
        st.title('')

if st.session_state['state'] == 'seller':
    dic = {}
    with st.form('seller',clear_on_submit=True):
        arr=st.columns(3)
        dic['Book name'] = arr[0].text_input("Book name")
        dic['Author name'] = arr[1].text_input("Author name")
        dic['Rent price'] = arr[0].text_input("Rent price")
        dic['Sell price'] = arr[1].text_input("Sell price")
        dic['Genre'] = arr[2].text_input("Genre")
        dic['Description'] = st.text_area("Description",height=200)
        files = arr[2].file_uploader("Add photos",accept_multiple_files=True)
        if st.form_submit_button("Upload"):
            try :
                eror=0
                for k in dic.keys():
                    if dic[k]=='':
                        st.error('All fields are mandatory')
                        eror=1
                        break
                dic['book_location']=[]
                if eror==0:
                    for no_,imag in enumerate(files):
                        could_filename = f"Books/{dic['Book name']}/{no_}.jpg"
                        blob = bucket.blob(could_filename)
                        blob.upload_from_string(imag.getvalue(), content_type="image/jpeg")
                        dic['book_location'].append(storage_py.child(could_filename).get_url(None))
                    db.collection('Costumers').document(st.session_state['user_details']['email']).collection('Uploaded Books').add(dic)
                st.success('Upload successfull')
                books_arr=[]
                get_books = db.collection_group('Uploaded Books')
                docs = get_books.stream()
                for doc in docs:
                    books_arr.append(doc.to_dict())
                st.session_state['chached_books'] = books_arr
            except Exception as e:
                st.error(json.loads(e.args[1])['error']['message'].replace('_', ' '))
