import re

text = r'''
    <meta content="always" name="referrer">
<script>
    var url = '';
    url += 'http://mp.weixin.qq.com/s?src=11&timestamp=1553504704&ver=1506&signature=ZQCxwQwyZdl9l5G2Ue9mL90DZjQLH8JsaU5BWMOSZi1VpX0Dkjv82EqQyuvEARuNJ41aHbzrww22mn-eHfCRdhFPr7-I54y6Z8fuB3kpk5XO43oWrNsD60ZK8P7WorVr&new=1';
    url += '';
    url += '';
    url += '';
    url += '';
    url += '';
    url += '';
    url += '';
    url += '';
    url += '';
    url += '';
    url.replace("@", "");
    window.location.replace(url)
</script>'''



print(text.split('url += \'')[1].replace("';", ""))