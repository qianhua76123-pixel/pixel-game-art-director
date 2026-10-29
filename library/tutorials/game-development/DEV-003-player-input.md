---
id: DEV-003
title: 读取玩家输入并驱动角色
category: game-development
source_url: https://docs.godotengine.org/en/4.5/getting_started/step_by_step/scripting_player_input.html
source_title: Listening to player input
author: Juan Linietsky, Ariel Manzur and the Godot community
license: CC-BY-3.0
license_url: https://creativecommons.org/licenses/by/3.0/
retrieved_at: '2026-10-29'
language: zh-CN+en
source_language: en
level: beginner
tags:
- Godot
- 输入
- 动作映射
- 角色控制
content_mode: licensed-fulltext-with-chinese-guide
version: Godot 4.5 documentation branch
prerequisites:
- 会给节点附加脚本
- 理解变量和函数
---

# 读取玩家输入并驱动角色

> 本文由 Godot 官方 4.5 版文档转换。下方中文导读、练习和验收是整理者的教学编排，英文正文是原教程主内容；不是官方中文逐句译文，也未声称已在引擎中执行全部练习。

## 适用任务

从按键状态读取开始，将输入、方向与运动参数连接起来。

## 前提

- 会给节点附加脚本
- 理解变量和函数

## 中文操作路线

1. 先运行原文已有旋转与前进脚本，确认每帧更新发生的位置。
2. 使用 Input.is_action_pressed 读取动作，而非把按键编码散落在各处。
3. 把左、右动作转成旋转方向，再将向前动作与当前朝向结合。
4. 检查同时按键、松开按键以及没有输入时的行为；保留 delta 对每秒速度的换算。
5. 俯视四向或八向移动改用 DEV-012 的 Input.get_vector 路线，不要把旋转式控制直接等同于四向角色。

## 图示怎么读

先沿英文正文的步骤阅读对应截图；截图来自同一版本页面，局部操作顺序以紧邻图片的文字为准。图片下载到本地，可离线打开并放大检查。截图中的示例美术用于说明引擎操作，不代表本库要求采用该画风。

## 动手练习

为原示例添加暂停运动动作，要求松开移动键后停止前进，但仍能按方向键旋转。

## 验收清单

- [ ] 输入动作名称与项目设置完全相同。
- [ ] 松开按键后没有残留速度。
- [ ] 改变运行帧率时，按住一秒得到的运动量基本一致。

## 版本与边界

本篇示范旋转式运动；角色碰撞响应需要另外阅读 CharacterBody2D 教程。

本次来源固定为 Godot 4.5 文档分支，抓取日期为 2026-10-29；它不是“当前最新版本”的声明。升级引擎时应重新核对节点名、属性名和 API。

## 原教程正文（英文，Markdown 转换）

### Listening to player input

Building upon the previous lesson, [Creating your first script](https://docs.godotengine.org/en/4.5/getting_started/step_by_step/scripting_first_script.html#doc-scripting-first-script), let's look
at another important feature of any game: giving control to the player.
To add this, we need to modify our `sprite_2d.gd` code.

![原教程图示：Listening to player input — scripting_first_script_moving_with_input.gif](../../assets/game-development/DEV-003/scripting_first_script_moving_with_input.gif)

You have two main tools to process the player's input in Godot:

1. The built-in input callbacks, mainly `_unhandled_input()`. Like
   `_process()`, it's a built-in virtual function that Godot calls every time
   the player presses a key. It's the tool you want to use to react to events
   that don't happen every frame, like pressing `Space` to jump. To learn
   more about input callbacks, see [Using InputEvent](https://docs.godotengine.org/en/4.5/tutorials/inputs/inputevent.html#doc-inputevent).
2. The `Input` singleton. A singleton is a globally accessible object. Godot
   provides access to several in scripts. It's the right tool to check for input
   every frame.

We're going to use the `Input` singleton here as we need to know if the player
wants to turn or move every frame.

For turning, we should use a new variable: `direction`. In our `_process()`
function, replace the `rotation += angular_speed * delta` line with the
code below.

```gdscript
var direction = 0
if Input.is_action_pressed("ui_left"):
    direction = -1
if Input.is_action_pressed("ui_right"):
    direction = 1

rotation += angular_speed * direction * delta
```

```csharp
var direction = 0;
if (Input.IsActionPressed("ui_left"))
{
    direction = -1;
}
if (Input.IsActionPressed("ui_right"))
{
    direction = 1;
}

Rotation += _angularSpeed * direction * (float)delta;
```

Our `direction` local variable is a multiplier representing the direction in
which the player wants to turn. A value of `0` means the player isn't pressing
the left or the right arrow key. A value of `1` means the player wants to turn
right, and `-1` means they want to turn left.

To produce these values, we introduce conditional statements and the use of `Input`.
A conditional statement starts with the `if` keyword in GDScript and ends with a colon. The
condition is specifically the expression between the keyword and the colon at
the end of the line.

To check if a key was pressed this frame, we call `Input.is_action_pressed()`.
The method takes a text string representing an input action and returns `true`
if the action is pressed, `false` otherwise.

The two actions we use above, "ui_left" and "ui_right", are predefined in every
Godot project. They respectively trigger when the player presses the left and
right arrows on the keyboard or left and right on a gamepad's D-pad.

Note

You can see and edit input actions in your project by going to
Project > Project Settings and clicking on the Input Map tab.

Finally, we use the `direction` as a multiplier when we update the node's
`rotation`: `rotation += angular_speed * direction * delta`.

Comment out the lines `var velocity = Vector2.UP.rotated(rotation) * speed` and `position += velocity * delta` like this:

```gdscript
#var velocity = Vector2.UP.rotated(rotation) * speed

#position += velocity * delta
```

```csharp
//var velocity = Vector2.Up.Rotated(Rotation) * _speed;

//Position += velocity * (float)delta;
```

This will ignore the code that moved the icon's position in a circle without user input from the previous exercise.

If you run the scene with this code, the icon should rotate when you press
`Left` and `Right`.

#### Moving when pressing "up"

To only move when pressing a key, we need to modify the code that calculates the
velocity. Uncomment the code and replace the line starting with `var velocity` with the code below.

```gdscript
var velocity = Vector2.ZERO
if Input.is_action_pressed("ui_up"):
    velocity = Vector2.UP.rotated(rotation) * speed
```

```csharp
var velocity = Vector2.Zero;
if (Input.IsActionPressed("ui_up"))
{
    velocity = Vector2.Up.Rotated(Rotation) * _speed;
}
```

We initialize the `velocity` with a value of `Vector2.ZERO`, another
constant of the built-in `Vector` type representing a 2D vector of length 0.

If the player presses the "ui_up" action, we then update the velocity's value,
causing the sprite to move forward.

#### Complete script

Here is the complete `sprite_2d.gd` file for reference.

```gdscript
extends Sprite2D

var speed = 400
var angular_speed = PI


func _process(delta):
    var direction = 0
    if Input.is_action_pressed("ui_left"):
        direction = -1
    if Input.is_action_pressed("ui_right"):
        direction = 1

    rotation += angular_speed * direction * delta

    var velocity = Vector2.ZERO
    if Input.is_action_pressed("ui_up"):
        velocity = Vector2.UP.rotated(rotation) * speed

    position += velocity * delta
```

```csharp
using Godot;

public partial class MySprite2D : Sprite2D
{
    private float _speed = 400;
    private float _angularSpeed = Mathf.Pi;

    public override void _Process(double delta)
    {
        var direction = 0;
        if (Input.IsActionPressed("ui_left"))
        {
            direction = -1;
        }
        if (Input.IsActionPressed("ui_right"))
        {
            direction = 1;
        }

        Rotation += _angularSpeed * direction * (float)delta;

        var velocity = Vector2.Zero;
        if (Input.IsActionPressed("ui_up"))
        {
            velocity = Vector2.Up.Rotated(Rotation) * _speed;
        }

        Position += velocity * (float)delta;
    }
}
```

If you run the scene, you should now be able to rotate with the left and right
arrow keys and move forward by pressing `Up`.

![原教程图示：Listening to player input — scripting_first_script_moving_with_input.gif](../../assets/game-development/DEV-003/scripting_first_script_moving_with_input.gif)

#### Summary

In summary, every script in Godot represents a class and extends one of the
engine's built-in classes. The node types your classes inherit from give you
access to properties, such as `rotation` and `position` in our sprite's case.
You also inherit many functions, which we didn't get to use in this example.

In GDScript, the variables you put at the top of the file are your class's
properties, also called member variables. Besides variables, you can define
functions, which, for the most part, will be your classes' methods.

Godot provides several virtual functions you can define to connect your class
with the engine. These include `_process()`, to apply changes to the node
every frame, and `_unhandled_input()`, to receive input events like key and
button presses from the users. There are quite a few more.

The `Input` singleton allows you to react to the player's input anywhere in
your code. In particular, you'll get to use it in the `_process()` loop.

In the next lesson, [Using signals](https://docs.godotengine.org/en/4.5/getting_started/step_by_step/signals.html#doc-signals), we'll build upon the relationship between
scripts and nodes by having our nodes trigger code in scripts.

---

## 来源、配图与授权

- 原文：[Listening to player input](https://docs.godotengine.org/en/4.5/getting_started/step_by_step/scripting_player_input.html)。
- 作者与署名：Juan Linietsky, Ariel Manzur and the Godot community。
- 文档许可：[CC BY 3.0](https://creativecommons.org/licenses/by/3.0/)；[官方仓库许可声明](https://github.com/godotengine/godot-docs/blob/4.5/README.md#license)。
- 许可全文：[godot-docs-4.5-LICENSE.txt](../../licenses/godot-docs-4.5-LICENSE.txt)。
- 本地原文主内容快照：[DEV-003.article.html](../../sources/game-development/DEV-003.article.html)。
- 变更：去除导航和用户评论入口，HTML 转 Markdown，图片改为相对路径，重复评级图标转成同义文字，新增中文导读、练习及验收。正文中的示例素材署名予以保留。
- 本整理稿的新增中文内容同样按 CC BY 3.0 提供，署名“Pixel Tutorial Library 整理者（Codex）”；不暗示原作者认可本整理稿。

| 本地图像 | 原图来源 | 图示语境 |
| --- | --- | --- |
| [scripting_first_script_moving_with_input.gif](../../assets/game-development/DEV-003/scripting_first_script_moving_with_input.gif) | [原图](https://docs.godotengine.org/en/4.5/_images/scripting_first_script_moving_with_input.gif) | 原教程图示：Listening to player input — scripting_first_script_moving_with_input.gif |
