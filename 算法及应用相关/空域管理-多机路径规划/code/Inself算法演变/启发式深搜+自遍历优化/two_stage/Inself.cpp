#include<math.h>
#include<queue>
#include<stack>
#include "Inself.h"//启发式深搜inspiredfs + 自遍历优化self

void Inself::InitInself(std::vector<std::vector<int>>& _maze)   //二维容器
{
	maze = _maze;
	inspire_num = 0;
	final_num = 0;
}

//只有启发式深搜
std::list<Point*> Inself::GetfPath(Point & startPoint, Point & endPoint, bool isIgnoreCorner)
{
	Point *result = findPath(startPoint, endPoint, isIgnoreCorner);
	std::list<Point *> path;
	//返回路径,若未找到,则返回空链表
	while (result)
	{
		path.push_front(new Point(result->x, result->y));//从前面插入,倒叙.
		result = result->parent;

	}

	return path;
}


//启发式深搜+自遍历优化
std::list<Point*> Inself::Self(Point & startPoint, Point & endPoint, bool isIgnoreCorner)
{
	int dx;
	int dy;
	//int degree_last;
	//int degree_tmp;
	//倒序的路径from启发式深搜：  ->parent当链表子节点用
	Point *result = findPath(startPoint, endPoint, isIgnoreCorner);
	std::list<Point *> path;
	while (result)//只要不为空，就遍历
	{
		//degree_last = 0;
		//degree_tmp = 0;
		Point *temp = result->parent;
		//记录初始方向，在第一个拐点之后开始：
		if (temp)
		{
			dx = temp->x - result->x;
			dy = temp->y - result->y;
		}
		while (temp)//第二层内循环,适当时修改result->parent，或及早break；
		{
			if ((temp->parent) && (temp->parent->x - temp->x == dx) && (temp->parent->y - temp->y == dy))
				;
			//degree_tmp = calDegree(result, tmp);
			//if()
			else if (isoneline(result, temp,isIgnoreCorner))
				{
					if (islineok(result, temp))
					{
						//连上
						extend(result, temp);
					}
					else
					{
						//遇障
						break;
					}
				}
			temp = temp->parent;
		}
		//加入path，因为倒叙，故从前面塞入
		path.push_front(new Point(result->x, result->y));//从前面插入,倒叙.
		//cout << result->x << "," << result->y << endl;
	
		final_num++;

		result = result->parent;
	}

	return path;
}





int Inself::calcG(Point * temp_start, Point * point)   //周围移动耗费
{
	int extraG = (abs(point->x - temp_start->x) + abs(point->y - temp_start->y) == 1) ? kCost1 : kCost2;  //判断是否为斜格
	int parentG = (point->parent == NULL) ? 0 : point->parent->G;
	return parentG + extraG;
}

int Inself::calcH(Point * point, Point * end)   //距离,计算算法仍有优化空间!
{
	return (abs(end->x - point->x) + abs(end->y - point->y))*kCost1;   //此处用简单算法:只可以平动不斜动
}

int Inself::calcF(Point * point)
{
	return point->G + point->H;
}

float  Inself::calDegree(Point *p1, Point *p2)
{
	return (float)(p2->y - p1->y)/(p2->x - p1->x);
}

bool  Inself::isoneline(const Point *p1, const Point *p2, bool isIgnoreCorner) //能否斜着移动
{
	if ((p2->x == p1->x)||(p2->y == p1->y)|| (abs(p2->y - p1->y) == abs(p2->x -p1->x)) )
	{
		if ((abs(p2->y - p1->y) == abs(p2->x - p1->x)))
			return isIgnoreCorner;
		else
			return true;
	}
	else
		return false;
}
bool  Inself::islineok(const Point *point, const Point *target)  //已通过isoneline，不再需要isIgnoreCorner，如果不能斜着移动，通过调用判断不会进入此函数
{
	int dx;
	int dy;
	if ((target->x - point->x) == 0)
		dx = 0;
	else
		dx = (target->x - point->x) / (abs(target->x - point->x));
	if ((target->y - point->y) == 0)
		dy = 0;
	else
		dy = (target->y - point->y) / (abs(target->y - point->y));
	int tx = point->x;
	int ty = point->y;
	while ((tx != target->x) || (ty != target->y))
	{
		tx = tx + dx;
		ty = ty + dy;
		if (maze[tx][ty]==1)//有障碍物
			return false;
	}

	return true;
}

void Inself::extend(Point *p1, Point *p2)
{
	Point *last = p1;
	int dx;
	int dy;
	if ((p2->x - p1->x) == 0)
		dx = 0;
	else
		dx = (p2->x - p1->x) / (abs(p2->x - p1->x));
	if ((p2->y - p1->y) == 0)
		dy = 0;
	else
		dy = (p2->y - p1->y) / (abs(p2->y - p1->y));
	int tempx = p1->x;
	int tempy = p1->y;
	while (tempx != p2->x || tempy != p2->y)
	{
		tempx += dx;
		tempy += dy;
		Point *tt = new Point(tempx, tempy);
		//衔接指针
		tt->parent = last->parent;
		last->parent = tt;

		last = last->parent; //此轮的tt
	}
	last->parent = p2->parent;//续上原p2后面的链路
}


Point * Inself::findPath(Point & startPoint, Point & endPoint, bool isIgnoreCorner)  //开辟新内存
{
	
	Point *curPoint = new Point(startPoint.x, startPoint.y);
	curPoint->parent = NULL;
	while (curPoint != NULL)
	{
		//第一次启发式深搜数目+1
		inspire_num++;

		maze[curPoint->x][curPoint->y] = 3;//标识走过路径
		auto surroundPoints = getSurroundPoints(curPoint, isIgnoreCorner);   //找周围的格子
		for (auto &target : surroundPoints)
		{
			target->parent = curPoint;   //当前点为其父点
			target->G = calcG(curPoint, target);
			target->H = calcH(target, &endPoint);
			target->F = calcF(target);
			maze[target->x][target->y] = 2;  //open but not went
			
		}


		Point *resPoint = isInList(curPoint, &endPoint); //判断endPoint是否在openList之中.
		if (resPoint)//endPoint is in openList
			return resPoint;   //开头处深拷贝,故返回resPoint节点,而非endPoint

		//找到F值最小的点
		if (!surroundPoints.empty())
		{
			
			curPoint = surroundPoints.front();
			for (auto &target : surroundPoints)
			{
				//openList.push_back(target);   //放入openList 中

				if (target->F < curPoint->F)
				{
					curPoint = target;
				}
			}
		}
		else
		{
			curPoint = curPoint->parent; //退回上一个

		}
	}
	return nullptr;
}



Point * Inself::isInList(Point * curPoint, const Point * point) const
{

	if (maze[point->x][point->y] == 2)
	{
		Point *p = new Point(point->x, point->y);
		p->parent = curPoint;
		return p;
	}
	return nullptr;
}


bool Inself::isCanreach(const Point * point, const Point * target, bool isIgnoreCorner, int safe_d) const  //加安全距离
{
	if (target->x<0 || target->x>maze.size() - 1
		|| target->y<0 || target->y>maze[0].size() - 1
		|| maze[target->x][target->y] == 1
		|| (target->x == point->x&&target->y == point->y)
		|| maze[target->x][target->y] == 3)//|| maze[target->x][target->y]==2,  2点也算在每个新店的周围点集内，可能存在绕远，但影响不大。
	{
		delete target;
		return false;
	}
	
	for (int i = -1; abs(i) < safe_d; i = (i < 0) ? (-i) : (-i - 1))//巧妙的探测
	{
		for (int j = -1; abs(j) < safe_d; j = (j < 0) ? (-j) : (-j - 1))
		{
			if (maze[target->x + i][target->y + j] == 1)
			{
				delete target;
				return false;
			}
		}
	}
	if (abs(point->x - target->x) + abs(point->y - target->y) == 1)
	{
		delete target;
		return true;
	}
	else
	{
		delete target;
		return isIgnoreCorner;// 判断斜对角是否绊住
	}
}


//探索周围可到达点
std::vector<Point*> Inself::getSurroundPoints(const Point * point, bool isIgnoreCorner)//clock 1:顺时针,左上角开始,2:逆时针
{
	//int temp_clock = 1;
	int temp_tmp_x = 0;
	int temp_tmp_y = 0;
	std::vector<Point *> surroundPoints;
	//for (int x = point->x - 1; x <= point->x + 1; x++)
	//	for (int y = point->y - 1; y <= point->y + 1; y++)

		for (int temp_ii = 0; temp_ii < 8; temp_ii++)
		{
			switch (temp_ii) {
			case 0:
				temp_tmp_x = -1;
				temp_tmp_y = 1;
				break;
			case 1:
				temp_tmp_x = 0;
				temp_tmp_y = 1;
				break;
			case 2:
				temp_tmp_x = 1;
				temp_tmp_y = 1;
				break;
			case 3:
				temp_tmp_x = 1;
				temp_tmp_y = 0;
				break;
			case 4:
				temp_tmp_x = 1;
				temp_tmp_y = -1;
				break;
			case 5:
				temp_tmp_x = 0;
				temp_tmp_y = -1;
				break;
			case 6:
				temp_tmp_x = -1;
				temp_tmp_y = -1;
				break;
			case 7:
				temp_tmp_x = -1;
				temp_tmp_y = 0;
				break;
			default:break;
			}
			if (isCanreach(point, new Point(point->x + temp_tmp_x, point->y + temp_tmp_y), isIgnoreCorner, safe_distance))
				surroundPoints.push_back(new Point(point->x + temp_tmp_x, point->y + temp_tmp_y));
		}

	return surroundPoints;
}