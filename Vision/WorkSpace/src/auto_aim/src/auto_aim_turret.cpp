#include <rclcpp/rclcpp.hpp>
#include <iostream>
#include <string>
#include "auto_aim_interfaces/msg/position.hpp"
#include "auto_aim_interfaces/msg/result_order.hpp"
#include <ctime>
#include <chrono>
#include <algorithm>

class AutoAimTurret : public rclcpp::Node
{
public:
//定义炮台类与节点，初始化时创建发布者与订阅者(话题通信)
  AutoAimTurret() : rclcpp::Node("auto_aim_turret")
  {
    //初始化时间戳
    last_msg_time = this->now();
    srand(time(NULL));
    position[0] = rand() % 720 + 1;
    position[1] = rand() % 1080 + 1;
    score = 0;
    speedx = 0;
    speedy = 0;
    x1 = 0;y1 = 0;x2 = 0;y2 = 0;
    // 看门狗定时器，检查退出
    watchdog_timer = this->create_wall_timer(std::chrono::seconds(1), std::bind(&AutoAimTurret::check_timeout, this));
    score_timer = this->create_wall_timer(std::chrono::seconds(1), std::bind(&AutoAimTurret::callback_calculate_score, this));
    aim_position = this->create_publisher<auto_aim_interfaces::msg::Position>("aim_position", 10);
    result_order = this->create_subscription<auto_aim_interfaces::msg::ResultOrder>("result_order", 10,
        std::bind(&AutoAimTurret::callback_result_order, this, std::placeholders::_1));
   
  }

private:
  void callback_result_order(const auto_aim_interfaces::msg::ResultOrder::SharedPtr msg)
  {
    //更新时间戳
    last_msg_time = this->now();
    //根据接收到的结果运动炮台，并发布新的目标位置
    //限制最大移动速度
    auto position_msg = auto_aim_interfaces::msg::Position();
    speedx = std::clamp((int)msg->x11, -12, 12);
    speedy = std::clamp((int)msg->y22, -12, 12);
    x11 = msg->x11;
    y22 = msg->y22;
    x1 = msg->x1;
    y1 = msg->y1;
    x2 = msg->x2;
    y2 = msg->y2;
    position[0] += speedx;
    position[1] += speedy;
    position_msg.position_x = position[0];
    position_msg.position_y = position[1];
    //发布现在炮台位置
    aim_position->publish(position_msg);
  }

  //计算分数的得分函数，每秒调用一次，根据当前炮台位置与目标位置的关系计算得分
  void callback_calculate_score()
  {

    //根据接收到的目标位置与当前炮台位置计算得分
    if(position[0] >= x1 && position[0] <= x2 && position[1] >= y1 && position[1] <= y2)
    {
      RCLCPP_INFO(this->get_logger(), "当前炮台位置：(%d, %d)", position[0], position[1]);
      RCLCPP_INFO(this->get_logger(), "目标位置范围：(%d, %d) - (%d, %d)", x1, y1, x2, y2);
      score += 1;
      RCLCPP_INFO(this->get_logger(), "命中目标！当前得分：%d", score);
    }
    else
    {
      RCLCPP_INFO(this->get_logger(), "当前炮台位置：(%d, %d)", position[0], position[1]);
      RCLCPP_INFO(this->get_logger(), "目标位置范围：(%d, %d) - (%d, %d)", x1, y1, x2, y2);
      RCLCPP_INFO(this->get_logger(), "未命中目标！当前得分：%d", score);
    }

    if(score >= 8)
    {
      RCLCPP_INFO(this->get_logger(), "恭喜你击败了Homelander!你赢了!");
      rclcpp::shutdown();
    } 
  }

//看门狗函数，用于检查函数是否退出超时
void check_timeout()
  {
    auto now = this->now();
    if ((now - last_msg_time).seconds() > 5.0) {
      RCLCPP_WARN(this->get_logger(), "你被Homelander用激光眼射中了!祝你下次好运!");
      rclcpp::shutdown();
    }
  }

//定义变量
private:
  rclcpp::Publisher<auto_aim_interfaces::msg::Position>::SharedPtr aim_position;
  rclcpp::Subscription<auto_aim_interfaces::msg::ResultOrder>::SharedPtr result_order;
  rclcpp::TimerBase::SharedPtr score_timer;
  rclcpp::TimerBase::SharedPtr watchdog_timer;
  rclcpp::Time last_msg_time;
  int x1 , x2, y1, y2;
  float x11, y22;
  int score;
  int position[2];
  int speedx;
  int speedy;
};

int main(int argc, char * argv[])
{

  rclcpp::init(argc, argv);
  auto node = std::make_shared<AutoAimTurret>();
  rclcpp::spin(node);
  return 0;
}