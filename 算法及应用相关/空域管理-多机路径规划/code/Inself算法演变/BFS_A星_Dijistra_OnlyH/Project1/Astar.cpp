#include "Astar.h"

int mode = 2; //1:广搜，2:A* , 3: dijistra（最小优先队列的标准F换为源距离G）  4:A* 启发项只有H
//仅1不排序;   2&4使用F，1&3使用G ；  4的F=H

//最小优先队列的历史最多数量
int max_num;
int max_num_temp;

void Astar::InitAstar(std::vector<std::vector<int>>& _maze)   //二维容器
{
	maze = _maze;
	check_num = 0;
	final_num = 0;

}


Point * Astar::find_GetPath(Point & startPoint, Point & endPoint, bool isIgnoreCorner)
{

	Point *curPointa=new Point(startPoint.x, startPoint.y);
	//重要
	curPointa->G = 0;

	curPointa->parent = NULL; //无用，默认null
	openlist.push_back(curPointa);

	while (!openlist.empty())
	{
		if(mode!=1)
		openlist.sort(less<Point *>());//升序,广搜中不含此步
		
		/*std::list<Point *>::iterator ita;
		for (ita = openlist.begin(); ita != openlist.end(); ita++)
		{
			cout << (*ita)->F << endl;
		}
		system("pause");*/

		Point *curPoint = openlist.front();  //找第一个
		openlist.pop_front();
		maze[curPoint->x][curPoint->y] = 7;//标识走过路径
		max_num_temp--;
		//test print
		//cout << curPoint->x << "," << curPoint->y << endl;
		
		auto surroundPoints = getSurroundPoints(curPoint, isIgnoreCorner);   //找周围的格子
		for (auto &target : surroundPoints)
		{
			target->G = calcG(target, curPoint);

			if(maze[target->x][target->y] == 0)
			{
				target->parent = curPoint;   //当前点为其父点
				//target->G = calcG(target, curPoint);
				target->H = calcH(target, &endPoint);
				target->F = calcF(target);
				maze[target->x][target->y] = 6;  //open but not went
				//加入openlist
				openlist.push_back(target);

				check_num++;
				max_num_temp++;
				if (max_num_temp > max_num)
					max_num = max_num_temp;
			}
			else if ((!openlist.empty()) && mode != 1 && maze[target->x][target->y] == 6) //检查更新&换父节点
			{
				std::list<Point *>::iterator it;
				for (it = openlist.begin(); it != openlist.end(); it++)
				{
					if ((*it)->x == target->x && (*it)->y == target->y)
					{
						if (((mode == 2||mode==4) && target->F < (*it)->F)||(mode ==3 && target->G < (*it)->G))   //多种模式，所以需提前算G
						{
							//需要更新,经测试，在list直接改不可取，全变成0，必须删了再加
							openlist.erase(it);
							target->parent = curPoint;   //当前点为其父点
							//target->G = calcG(target, curPoint);
							target->H = calcH(target, &endPoint);
							target->F = calcF(target);
							openlist.push_back(target);
						}
						break;
					}
				}
			}
		}


		Point *resPoint = isInList(curPoint, &endPoint); //判断endPoint是否在openList之中.
		if (resPoint)//endPoint is in openList
			return resPoint;   //开头处深拷贝,故返回resPoint节点,而非endPoint

	}
	return nullptr;
}



std::list<Point*> Astar::GetPath(Point & startPoint, Point & endPoint, bool isIgnoreCorner)
{
	Point *result = find_GetPath(startPoint, endPoint, isIgnoreCorner);
	std::list<Point *> path;
	//返回路径,若未找到,则返回空链表
	while (result)
	{
		path.push_front(new Point(result->x, result->y));//从前面插入,倒叙.
		final_num++;
		result = result->parent;
	}

	return path;
}


///////////////////////////////////////////////////////////////////////////////////////

int Astar::calcG(Point * temp_start, Point * point)   //周围移动耗费,b->a
{
	int extraG = (abs(point->x - temp_start->x) + abs(point->y - temp_start->y) == 1) ? kCost1 : kCost2;  //判断是否为斜格
	int parentG = (point->parent == NULL) ? 0 : point->parent->G;
	return parentG + extraG;
}

int Astar::calcH(Point * point, Point * end)   //距离,计算算法仍有优化空间!
{
	return (abs(end->x - point->x) + abs(end->y - point->y))*kCost1;   //此处用简单算法:只可以平动不斜动
}

int Astar::calcF(Point * point)
{
	if(mode == 4)
		return   point->H;
	else
		return   point->G + point->H;
}



Point * Astar::isInList(Point * curPoint, const Point * point) const
{

	if (maze[point->x][point->y] == 6|| maze[point->x][point->y] == 7)
	{
		Point *p = new Point(point->x, point->y);
		p->parent = curPoint;
		return p;
	}
	return nullptr;
}


bool Astar::isCanreach(const Point * point, const Point * target, bool isIgnoreCorner, int safe_d) const  //加安全距离
{
	if (target->x<0 || target->x>maze.size() - 1
		|| target->y<0 || target->y>maze[0].size() - 1
		|| maze[target->x][target->y] == 1
		|| (target->x == point->x&&target->y == point->y)
		|| maze[target->x][target->y] == 7)  //7:closed   //|| maze[target->x][target->y]==2,  2点也算在每个新店的周围点集内，可能存在绕远，但影响不大。
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
std::vector<Point*> Astar::getSurroundPoints(const Point * point, bool isIgnoreCorner)
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