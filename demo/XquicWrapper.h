#ifndef XQUIC_WRAPPER_H_INCLUDED
#define XQUIC_WRAPPER_H_INCLUDED

#include <stdint.h>
#include <xquic/xquic_typedef.h>

#ifdef __cplusplus
extern "C" {
#endif
// 客户端连接服务器
XQC_EXPORT_PUBLIC_API 
void XQUIC_Connect(const char* host, int port);
XQC_EXPORT_PUBLIC_API
void XQUIC_Disconnect();

// 服务器侦听客户端连接
XQC_EXPORT_PUBLIC_API
int XQUIC_Listen(int port);
XQC_EXPORT_PUBLIC_API
void XQUIC_Unlisten();

// 发送数据
XQC_EXPORT_PUBLIC_API
int XQUIC_Send(void* conn, const uint8_t* data, int length);

// 接收回调函数类型定义
typedef void (*ReceiveCallback)(const uint8_t* data, int length, void* userData);

// 设置接收回调
XQC_EXPORT_PUBLIC_API
void XQUIC_SetReceiveCallback(void* conn, ReceiveCallback callback, void* userData);


#ifdef __cplusplus
}
#endif

#endif 