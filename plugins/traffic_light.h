#ifndef TF_PLUGIN_H
#define TF_PLUGIN_H

#include <ros/ros.h>
#include <std_msgs/UInt8.h>

#include <gazebo/gazebo.hh>
#include <gazebo/rendering/Visual.hh>
#include <gazebo/common/Plugin.hh>

namespace gazebo
{

class Wr8TrafficLightPlugin : public VisualPlugin
{
public:
    Wr8TrafficLightPlugin();
    virtual ~Wr8TrafficLightPlugin();
    void Load(rendering::VisualPtr visual, sdf::ElementPtr);
    void topicCallback(const std_msgs::UInt8& msg);
protected:
private:
    enum Sphere_t { NONE, TOP, BOT };
    enum States_t { NO_COLORS, RED, GREEN };

    void OnCmdTL();
    void OnUpdate();

    ros::NodeHandle* node_handler_;
    ros::Subscriber subscriber_;

    rendering::VisualPtr model_;
    std::string tf_name_;
    Sphere_t sphere_type;
};

} // end namespace Gazebo
#endif // TF_PLUGIN_H
