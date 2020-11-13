clc
clear all

set(figure,'units','normalized','position',[0.1 0.1 0.8 0.8]);
% axis([0 500 0 700]);
axis equal
xlabel('x');
ylabel('y');
grid on

%读路径
fid = fopen('path1.txt');
path = fscanf(fid, '%f');
i = 1;
line(path(i),path(i+1),'color','g', 'marker','.','markersize',20);%[0.8 1 1]
line(path(length(path) - 1),path(length(path)),'color','g', 'marker','.','markersize',20);
while(i < length(path) - 2)
    line([path(i),path(i+2)],[path(i+1),path(i+3)],'color','r','linewidth',2);
    i = i + 2;
end


%读路径
fid = fopen('path2.txt');
path = fscanf(fid, '%f');
i = 1;
line(path(i),path(i+1),'color','g', 'marker','.','markersize',20);%[0.8 1 1]
line(path(length(path) - 1),path(length(path)),'color','g', 'marker','.','markersize',20);
while(i < length(path) - 2)
    line([path(i),path(i+2)],[path(i+1),path(i+3)],'color','b','linewidth',2);
    i = i + 2;
end


%读障碍
fid = fopen('rock.txt');
rock = fscanf(fid, '%d');
i = 1;
while(i < length(rock))
    rectangle('Position', [rock(i),rock(i+1),1,1], 'FaceColor','k');
    i = i + 2;
end



axis([0 100 0 100]);

% %运动动画
% i = 1
% tank = line(path(i),path(i+1),'color','r', 'marker','.','markersize',20);
% while(i < length(path))
%     t1=clock;
%     set(tank,'xdata',path(i),'ydata',path(i+1));
%     i = i + 2;
%     pause(0.02);
% end