#include "iWatch.h"

static unsigned char code T_REX[] = {
	21, 24,
	0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xFE,0xFF,0xF3,0xF3,0xFF,0x7F,
	0x7F,0x7F,0x7F,0x7F,0x7E,0xFF,0xFF,0xF0,0xE0,0xE0,0xF0,0xF8,0xF8,0xFE,0xFF,0xFF,
	0xFF,0xFF,0xFF,0xFF,0x19,0x19,0x39,0x01,0x00,0x00,0x00,0x01,0x03,0x07,0x0F,0xFF,
	0xFF,0xDF,0x1F,0x1F,0xFF,0xFF,0xC7,0x03,0x01,0x00,0x00,0x00,0x00,0x00,0x00/*"D:\ͼƬ\src=http___i-1.edowning.net_2021_8_9_20468a9e-48c9-49bd-a2ee-363bc86db125.jpg&refer=http___i-1.edowning.bmp",0*/
	/* (21 X 24 )*/
};

static unsigned char code TREE1[] = {
	14, 24,
	0x00,0x00,0x00,0x00,0x00,0xE0,0xF0,0xF0,0xE0,0x00,0x00,0xC0,0xC0,0x80,0xFE,0xFF,
	0xFF,0x80,0x00,0xFF,0xFF,0xFF,0xFF,0xE0,0xF0,0x7F,0x7F,0x3F,0x01,0x03,0x07,0x07,
	0x07,0xFF,0xFF,0xFF,0xFF,0x00,0x00,0x00,0x00,0x00,/*"D:\ͼƬ\TREE.BMP",0*/
	/* (14 X 24 )*/
};

static unsigned char code TREE2[] = {
	12, 16, 
	0xE0,0xE0,0x00,0x00,0xFC,0xFE,0xFC,0x80,0xC0,0xFC,0x7C,0x00,0x07,0x0F,0x1E,0x1C,
	0xFF,0xFF,0xFF,0x01,0x01,0x00,0x00,0x00,/*"D:\ͼƬ\TREE2.BMP",0*/
	/* (12 X 16 )*/
};


static unsigned char code GROUND1[] = {
	128, 16,
	0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,
	0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,
	0x80,0x80,0x80,0x40,0x40,0x40,0x40,0x40,0x40,0x60,0x20,0x30,0x10,0x10,0x08,0x08,
	0x08,0x08,0x04,0x04,0x04,0x04,0x04,0x0C,0x08,0x18,0x30,0x20,0x20,0x40,0x40,0x40,
	0x40,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,
	0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x40,0x40,0x40,0x40,0x20,0x20,0x20,0x20,
	0x20,0x20,0x20,0xA0,0x20,0x20,0x20,0x20,0x20,0x60,0x40,0xC0,0x80,0x80,0x80,0x80,
	0x80,0x80,0x80,0xC0,0x40,0x40,0x40,0x40,0x40,0x40,0x40,0x40,0x40,0x40,0xC0,0x80,
	0x00,0x00,0x00,0x00,0x02,0x02,0x02,0x00,0x00,0x10,0x10,0x10,0x10,0x00,0x00,0x00,
	0x02,0x02,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x10,0x10,0x10,0x02,0x00,0x00,0x00,
	0x00,0x00,0x00,0x40,0x40,0x40,0x00,0x08,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x04,
	0x06,0x02,0x02,0x02,0x00,0x00,0x00,0x00,0x00,0x20,0x00,0x00,0x00,0x00,0x00,0x20,
	0x20,0x40,0x40,0x40,0x40,0x40,0x00,0x00,0x20,0x20,0x00,0x00,0x00,0x00,0x00,0x04,
	0x00,0x00,0x00,0x00,0x02,0x02,0x02,0x02,0x00,0x80,0x80,0x80,0x00,0x00,0x00,0x00,
	0x08,0x08,0x00,0x00,0x00,0x00,0x00,0x20,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
	0x00,0x00,0xC2,0x40,0x00,0x00,0x00,0x00,0x00,0x04,0x04,0x04,0x00,0x00,0x00,0x00,/*"D:\ͼƬ\GROUND1.BMP",0*/
	/* (128 X 16 )*/
};
static unsigned char code GROUND2[] = {
	128, 16,	
	0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0xC0,0x60,0x30,0x10,0x10,0x10,0x10,
	0x10,0x10,0x10,0x30,0x20,0x60,0xC0,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,
	0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
	0x00,0x00,0x00,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0xC0,0x60,0x30,0x10,0x10,0x10,
	0x18,0x08,0x38,0xE0,0x80,0x00,0x00,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,
	0x80,0x80,0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x80,
	0x80,0xC0,0x40,0x40,0x40,0x40,0x40,0x40,0x40,0x40,0xC0,0x80,0x80,0x80,0x80,0x80,
	0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,
	0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x14,0x04,0x04,0x04,0x44,0x00,0x00,
	0x08,0x00,0x00,0x00,0x00,0x10,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x14,0x10,
	0x10,0x10,0x00,0x00,0x00,0x00,0x00,0x41,0x41,0x41,0x41,0x41,0x01,0x01,0x01,0x01,
	0x01,0x01,0x01,0x01,0x00,0x00,0x10,0x20,0x60,0x00,0x00,0x00,0x00,0x00,0x00,0x40,
	0x40,0x00,0x00,0x00,0x00,0x01,0x01,0x01,0x00,0x00,0x08,0x08,0x08,0x00,0x08,0x00,
	0x00,0x00,0x00,0x01,0x01,0x03,0x02,0x03,0x01,0x41,0x01,0x01,0x11,0x11,0x11,0x11,
	0x10,0x10,0x10,0x00,0x00,0x00,0x00,0x00,0x10,0x00,0x00,0x00,0x00,0x00,0x08,0x00,
	0x04,0x00,0x00,0x20,0x20,0x00,0x00,0x00,0x08,0x00,0x00,0x00,0x00,0x00,0x00,0x00,/*"D:\ͼƬ\GROUND2.BMP",0*/
	/* (128 X 16 )*/
};

static unsigned char code Icon[] = {
	48, 48,
	0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
	0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x80,0xC0,0xE0,0x60,0xE0,0xE0,0xE0,0xE0,
	0xE0,0xE0,0xE0,0xE0,0xE0,0xC0,0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
	0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
	0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xFF,0xFF,0xFF,0xFE,0xFE,0xFF,0xFF,0x9F,
	0x9F,0x9F,0x9F,0x9F,0x1F,0x1F,0x1F,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
	0x00,0x00,0x00,0xF8,0xF0,0x00,0x80,0x80,0x00,0x00,0xFF,0xF8,0xE0,0xE0,0xC0,0xC0,
	0xC0,0xE0,0xF0,0xF8,0xF8,0xFC,0xFC,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0x18,0x18,
	0x38,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
	0x1F,0x30,0x30,0xFF,0xFF,0x18,0x1F,0x0F,0x00,0x00,0x01,0x07,0x07,0x0F,0x3F,0x3F,
	0x7F,0xFF,0xFF,0xFF,0xFF,0x7F,0x7F,0xFF,0xFF,0xFF,0x3F,0x0F,0x03,0x03,0x00,0x00,
	0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x7C,0xFC,0xC0,0xFE,0xFE,0x80,0xF0,0xF0,
	0x04,0x04,0x14,0x07,0x07,0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x04,
	0x04,0x1F,0x1F,0x17,0x05,0x04,0x04,0x05,0x1F,0x1F,0x14,0x04,0x04,0x04,0x04,0x04,
	0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x07,0x1F,0x05,0x05,0x04,
	0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x01,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
	0x00,0x00,0x00,0x00,0x00,0x08,0x08,0x00,0x00,0x00,0x08,0x08,0x08,0x00,0x00,0x00,
	0x00,0x00,0x01,0x01,0x01,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,/*"D:\ͼƬ\T-REX.bmp",0*/
	/* (48 X 48 )*/
};
static t_psWidget label_score, label_game;
static t_psWidget trex, tree1, tree2, tree3, bg1, bg2;
static t_psGroup group1;
static unsigned char xdata game_start = 0;
static unsigned char xdata collided = 0;
static unsigned int xdata score = 0;
static unsigned char xdata collison_cnt = 0;

/**
  * @brief  ҳ���ʼ���¼�
  * @param  ��
  * @retval ��
  */
static void Setup(unsigned char condition)
{
	label_score = og_label_create(FONT_ASCII_5X7, 0, 0);
	label_game = og_label_create(FONT_ASCII_7X8, 34, -8);
	og_label_setText(label_game, "Game over!");
	og_widget_setAlignment(label_game, ALIGN_HORIZONMID);
	og_widget_setShow(label_game, 0);
	trex = og_bmp_create((t_psBMP)T_REX, 20, 36);
	tree1 = og_bmp_create((t_psBMP)TREE1, 96, 36);
	tree2 = og_bmp_create((t_psBMP)TREE2, 140, 44);
	tree3 = og_bmp_create((t_psBMP)TREE2, 240, 44);
	bg1 = og_bmp_create((t_psBMP)GROUND1, 0, 48);
	bg2 = og_bmp_create((t_psBMP)GROUND2, 128, 48);
	group1 = og_group_create(8);
	og_group_addWidget(group1, label_score, 0);
	og_group_addWidget(group1, label_game, 0);
	og_group_addWidget(group1, trex, 0);
	og_group_addWidget(group1, tree1, 0);
	og_group_addWidget(group1, tree2, 0);
	og_group_addWidget(group1, tree3, 0);
	og_group_addWidget(group1, bg1, 0);
	og_group_addWidget(group1, bg2, 0);
	og_group_setPosOffset(group1, 0, 64);
	og_group_addAnimOffset(group1, 0, -64, ANIM_TIME_NORM, ANIM_NULL_CB);
	srand((time.second << 8) | time.minute);		//�����������Ϊ���������
	game_start = 1;
	collided = 0;
	score = 0;
	collison_cnt = 0;
}
static void delet(void)
{
	og_group_delet(group1);
	pageSetStatus(page_trexrunner, PAGE_IDLE);
}
/**
  * @brief  ҳ���˳��¼�
  * @param  ��
  * @retval ��
  */
static void Exit(unsigned char condition)
{
	og_group_addAnimOffset(group1, 0, 64, ANIM_TIME_NORM, delet);
}
#define	ABS(a, b)	(a<b?(b-a):(a-b))
/**
  * @brief  ҳ��ѭ��ִ�е�����
  * @param  ��
  * @retval ��
  */
static void Loop()
{
	if(pageExecuteRate(&Rate50Hz))
	{
		iWatchKeepActive();
		if(game_start)
		{
			if(collided == 1)
			{
				static unsigned int t_cnt = 0;
				if(t_cnt % 5 == 0)
				{
					if(trex->config & WIDGET_SHOW)
						trex->config &= ~WIDGET_SHOW;
					else
						trex->config |= WIDGET_SHOW;
				}
				if(t_cnt++ == 100)
				{
					t_cnt = 0;
					trex->config |= WIDGET_SHOW;
					collided = 0;
				}
			}
			else
			{
				//��ײ���
				if((tree1->x - trex->x < trex->w) && (tree1->x - trex->x > -tree1->w))
				{
					if(tree1->y - trex->y < 20)//tree1->h
						collided = 1;
				}
				if(trex->x - tree1->x == tree1->w)
				{
					if(collided == 0)
						score++;
				}
				if((tree2->x - trex->x < trex->w) && (tree2->x - trex->x > -tree2->w))
				{
					if(tree2->y - trex->y < 15)//tree2->h
						collided = 1;
				}
				if(trex->x - tree2->x == tree2->w)
				{
					if(collided == 0)
						score++;
				}
				if((tree3->x - trex->x < trex->w) && (tree3->x - trex->x > -tree3->w))
				{
					if(tree3->y - trex->y < 20)//tree3->h
						collided = 1;
				}
				if(trex->x - tree3->x == tree3->w)
				{
					if(collided == 0)
						score++;
				}
				if(collided == 1)
				{
					Bee();
					if(++collison_cnt == 3)
					{
						game_start = 0;
						og_widget_setShow(label_game, 1);
						og_anim_create(label_game, label_game->x, 24, ANIM_TIME_NORM, ANIM_NULL_CB);
					}
				}
			}
			if(tree1->x-- < -12)
			{
				tree1->x = 128 + (rand() % 128);
			}
			if(tree2->x-- < -12)
			{
				tree2->x = 128 + (rand() % 128);
			}
			if(tree3->x-- < -12)
			{
				tree3->x = 128 + (rand() % 128);
			}
			if(bg1->x-- == -128)
				bg1->x = 128;
			if(bg2->x-- == -128)
				bg2->x = 128;
			lablel_printf(label_score, "%u", score);
		}
	}
}
void anim_fall(void)
{
	og_anim_create(trex, 20, 36, 350, ANIM_NULL_CB);
}
void anim_jump(void)
{
	og_anim_create(trex, 20, 4, 300, anim_fall);
}
/**
  * @brief  ҳ���¼�
  * @param  btn:�����¼��İ���
  * @param  event:�¼����
  * @retval ��
  */
static void Event(unsigned char event)
{
	if(event == KEY1_PRESSED)
		pageShift(page_menu, PAGE_RETURN);
	else if(event == KEY3_PRESSED)
	{
		anim_jump();
	}
	else if(event == KEY4_PRESSED)
	{
		//og_anim_create(text2, 48, 0, ANIM_TIME_NORM, ANIM_NULL_CB);
	}
}
void pageRegister_page_trexrunner(unsigned char pageID)
{
	pageRegister(pageID, "T-REX RUNNER", Icon, Setup, Loop, Exit, Event);
}