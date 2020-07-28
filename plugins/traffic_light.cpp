#include "traffic_light.h"
#include <std_msgs/String.h>
#include <gazebo/physics/physics.hh>

static const char* TOP_SPHERE_NAME = "topSphere";
static const char* BOT_SPHERE_NAME = "bottomSphere";

static const char* MATERIAL_RED = "Gazebo/Red";
static const char* MATERIAL_GREEN = "Gazebo/Green";
static const char* MATERIAL_GREY = "Gazebo/Grey";

namespace gazebo
{
    GZ_REGISTER_VISUAL_PLUGIN(Wr8TrafficLightPlugin)

    Wr8TrafficLightPlugin::Wr8TrafficLightPlugin(): node_handler_(nullptr),
        sphere_type(NONE)
    {
        ROS_INFO("Traffic Light Plugin is created!");
    }

    Wr8TrafficLightPlugin::~Wr8TrafficLightPlugin()
    {
        node_handler_->shutdown();
        if(node_handler_ != nullptr)
        {
            delete node_handler_;
        }
        ROS_INFO("Destructor is called");
    }

    void Wr8TrafficLightPlugin::Load(rendering::VisualPtr visual, sdf::ElementPtr)
    {
        // Parse input arguments
        this->model_ = visual;
        std::string visual_name = this->model_->Name();
        ROS_INFO("Visual full name is %s:", visual_name.c_str());
        signed int find_result;
        if((find_result = visual_name.find(TOP_SPHERE_NAME)) != -1){
            ROS_INFO("- link name is %s", TOP_SPHERE_NAME);
            sphere_type = Sphere_t::TOP;
        }
        else if((find_result = visual_name.find(BOT_SPHERE_NAME)) != -1)
        {
            ROS_INFO("- link name is %s", BOT_SPHERE_NAME);
            sphere_type = Sphere_t::BOT;
        }
        else
        {
            return;
        }
        this->model_->SetMaterial(MATERIAL_GREY);
        tf_name_ = visual_name.substr(0, find_result - 2);
        ROS_INFO("- tf name is %s", tf_name_.c_str());

        // If ROS is initialized we can create instance of ros::NodeHandle,
        //otherwise (when we run only gazebo) we can't
        if( !ros::isInitialized() )
        {
            ROS_WARN("ROS has not beed initialized, don't subscribe!");
        }
        else
        {
            node_handler_ = new ros::NodeHandle();
            subscriber_ = node_handler_->subscribe(tf_name_ + "_topic", 10,
                          &Wr8TrafficLightPlugin::topicCallback, this);
        }
    }

    void Wr8TrafficLightPlugin::topicCallback(const std_msgs::UInt8& msg)
    {
        ROS_DEBUG("I heard: [%u]", msg.data);
        if(States_t::RED == msg.data)
        {
            if(Sphere_t::TOP == sphere_type)
                this->model_->SetMaterial(MATERIAL_RED);
            else if(Sphere_t::BOT == sphere_type)
                this->model_->SetMaterial(MATERIAL_GREY);
        }
        else if(States_t::GREEN == msg.data)
        {
            if(Sphere_t::TOP == sphere_type){
                this->model_->SetMaterial(MATERIAL_GREY);
            }else if(Sphere_t::BOT == sphere_type){
                this->model_->SetMaterial(MATERIAL_GREEN);}
        }
        else
        {
            this->model_->SetMaterial(MATERIAL_GREY);
        }
    }
}
