#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>
#include <netinet/ip.h>
#include <netinet/ip_icmp.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

typedef unsigned char u8;
typedef unsigned short int u16;

struct icmp_header {
  unsigned char type;
  unsigned char code;
  unsigned short checksum;
  unsigned short id;
  unsigned short seq;
};

unsigned short in_cksum(unsigned short *buf, int len) {
  unsigned long sum = 0;
  for (; len > 0; len--) {
    sum += *buf++;
  }
  sum = (sum >> 16) + (sum & 0xffff);
  sum += (sum >> 16);
  return (unsigned short)(~sum);
}

int main(int argc, char **argv) {
  if (argc != 3) {
    fprintf(stderr, "Usage: %s <public_ip> <private_ip>\n", argv[0]);
    return 1;
  }

  unsigned long daddr = inet_addr(argv[1]);
  unsigned long saddr = inet_addr(argv[2]);

  int sockfd = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP);
  if (sockfd < 0) {
    perror("could not create socket");
    return 1;
  }

  int on = 1;
  if (setsockopt(sockfd, IPPROTO_IP, IP_HDRINCL, (const char*)&on, sizeof(on)) == -1) {
    perror("setsockopt");
    close(sockfd);
    return 1;
  }

  if (setsockopt(sockfd, SOL_SOCKET, SO_BROADCAST, (const char*)&on, sizeof(on)) == -1) {
    perror("setsockopt");
    close(sockfd);
    return 1;
  }

  int payload_size = 0;
  int packet_size = sizeof(struct iphdr) + sizeof(struct icmp_header) + payload_size;

  char *buffer = (char*) malloc(packet_size);
  char *packet = (char*) malloc(packet_size);
  if (!packet || !buffer) {
    perror("out of memory");
    free(packet);
    free(buffer);
    close(sockfd);
    return 1;
  }

  memset(packet, 0, packet_size);
  memset(buffer, 0, packet_size);

  struct iphdr* ip = (struct iphdr*) packet;
  struct icmp_header* icmphdr = (struct icmp_header*) (packet + sizeof(struct iphdr));

  ip->version = 4;
  ip->ihl = 5;
  ip->tos = 0;
  ip->tot_len = htons(packet_size);
  ip->id = rand();
  ip->frag_off = 0;
  ip->ttl = 255;
  ip->protocol = IPPROTO_ICMP;
  ip->saddr = saddr;
  ip->daddr = daddr;

  icmphdr->type = ICMP_ECHO;
  icmphdr->code = 0;
  icmphdr->id = htons(5);
  icmphdr->seq = htons(66);
  icmphdr->checksum = 0;

  struct sockaddr_in servaddr;
  servaddr.sin_family = AF_INET;
  servaddr.sin_addr.s_addr = daddr;
  memset(&servaddr.sin_zero, 0, sizeof(servaddr.sin_zero));

  int ls = sizeof(servaddr);
  int rf;

  for (int sent = 0; sent < 100; sent++) {
    icmphdr->checksum = 0;
    icmphdr->checksum = in_cksum((unsigned short*) icmphdr, sizeof(struct icmp_header) + payload_size);

    if (sendto(sockfd, packet, packet_size, 0, (struct sockaddr*)&servaddr, sizeof(servaddr)) == -1) {
      perror("sendto failed");
      break;
    }

    rf = recvfrom(sockfd, buffer, packet_size, 0, (struct sockaddr*)&servaddr, &ls);
    if (rf == -1) {
      perror("recvfrom failed");
      break;
    }

    struct icmp_header* icmp_response = (struct icmp_header*)(buffer + sizeof(struct iphdr));
    if (icmp_response->type == ICMP_ECHOREPLY) {
      printf("Received ICMP Echo Reply\n");
    }

    usleep(500000);
  }

  free(buffer);
  free(packet);
  close(sockfd);
  return 0;
}