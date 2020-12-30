<?php

class Iciba
{
    private $appid = '';
    private $appsecret = '';
    private $template_id = '';
    private $access_token = '';

    // 构造函数
    function __construct($wechat_config){
        $this->appid = trim($wechat_config['appid']);
        $this->appsecret = trim($wechat_config['appsecret']);
        $this->template_id = trim($wechat_config['template_id']);
    }

    // HTTP请求
    private function https_request($url, $data = null){
        $curl = curl_init();
        curl_setopt($curl, CURLOPT_URL, $url);
        curl_setopt($curl, CURLOPT_HEADER, 0);
        curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, 0);
        curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, 0);
        if (!empty($data)) {
            curl_setopt($curl, CURLOPT_POST, 1);
            curl_setopt($curl, CURLOPT_POSTFIELDS, $data);
        }
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
        $output = curl_exec($curl);
        curl_close($curl);
        return $output;
    }
    
    // 错误代码
    private function get_error_info($errcode){
        $infoList = [
            40013 => '不合法的 AppID ，请开发者检查 AppID 的正确性，避免异常字符，注意大小写',
            40125 => '无效的appsecret',
            41001 => '缺少 access_token 参数',
            40003 => '不合法的 OpenID ，请开发者确认 OpenID （该用户）是否已关注公众号，或是否是其他公众号的 OpenID',
            40037 => '无效的模板ID',
        ];
        return array_key_exists($errcode, $infoList) ? $infoList[$errcode] : 'unknown error';
    }

    // 打印日志
    private function print_log($data, $openid=null){
        $errcode = $data['errcode'];
        $errmsg = $data['errmsg'];
        if($errcode == 0){
            print_r(" [INFO] send to $openid is success\r\n");
        }else{
            // Windows环境下执行此命令解决中文乱码
            system('chcp 65001');
            $errinfo = $this->get_error_info($errcode);
            print_r(" [ERROR] ($errcode) $errmsg - $errinfo\r\n");
            if(!empty($openid)){
                print_r(" [ERROR] send to $openid is error\r\n");
            }
            exit();
        }
    }

    // 获取access_token
    private function get_access_token($appid, $appsecret){
        $url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=$appid&secret=$appsecret";
        $data = json_decode($this->https_request($url), true);
        if(array_key_exists('errcode', $data)){
            $this->print_log($data);
        }else{
            $this->access_token = $data['access_token'];
        }
    }

    // 获取用户列表
    private function get_user_list(){
        if($this->access_token == ''){
            $this->get_access_token($this->appid, $this->appsecret);
        }
        $access_token = $this->access_token;
        $url = "https://api.weixin.qq.com/cgi-bin/user/get?access_token=$access_token&next_openid=";
        $result = $this->https_request($url);
        $data = json_decode($result, true);
        if(array_key_exists('errcode', $data)){
            $this->print_log($data);
        }else{
            $openids = $data['data']['openid'];
            return $openids;
        }
    }

    // 发送消息
    private function send_msg($openid, $template_id, $iciba_everyday){
        $msg = [
            'touser'        =>  $openid,
            'template_id'   =>  $template_id,
            'url'           =>  $iciba_everyday['fenxiang_img'],
            'data'          =>  [
                'content'       =>  [
                    'value' =>  $iciba_everyday['content'],
                    'color' =>  '#0000CD'
                ],
                'note'          =>  [
                    'value' =>  $iciba_everyday['note']
                ],
                'translation'   =>  [
                    'value' =>  $iciba_everyday['translation']
                ]
            ]
        ];
        $json = json_encode($msg, JSON_UNESCAPED_UNICODE);
        if($this->access_token == ''){
            $this->get_access_token($this->appid, $this->appsecret);
        }
        $access_token = $this->access_token;
        $url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=$access_token";
        $result = $this->https_request($url, $json);
        return json_decode($result, true);
    }

    // 获取爱词霸每日一句
    private function get_iciba_everyday(){
        $url = "http://open.iciba.com/dsapi/";
        $result = $this->https_request($url);
        return json_decode($result, true);
    }

    // 为设置的用户列表发送消息
    private function send_everyday_words($openids){
        $everyday_words = $this->get_iciba_everyday();
        foreach ($openids as $openid) {
            $openid = trim($openid);
            $data = $this->send_msg($openid, $this->template_id, $everyday_words);
            $this->print_log($data, $openid);
        }
    }

    // 执行
    public function run($openids=[]){
        // 如果openids为空，则遍历用户列表
        $openids = empty($openids) ? $this->get_user_list() : $openids;
        // 根据openids对用户进行群发
        $this->send_everyday_words($openids);
    }
}


