'use client'

import { IconArrowRight, IconPlus } from '@tabler/icons-react';
import { ActionIcon, Paper, Textarea, useMantineTheme } from '@mantine/core';
import { MenuDropDown } from './menu-with-dropdown';
import { Dropzone, FileWithPath } from '@mantine/dropzone';
import { useState } from 'react';
import { FilePreviewCard } from './file-preview-card';

export function InputWithButton() {
  const theme = useMantineTheme();

  const [fileArray, setFileArray] = useState<FileWithPath[]>([]);

  return (
    <Dropzone 
      onDrop={(newFiles) => setFileArray( (previousArray) => [...previousArray, ...newFiles])} 
      activateOnClick={false}
    >
      <Paper
        radius="lg"
        withBorder
        p="md"
        >
          <ul className="flex flex-wrap gap-2">
            { fileArray.map((file, index) => (
              <li key={index}>
                <FilePreviewCard 
                  file={file} 
                  onRemove={() => setFileArray(prev => prev.filter((_, i) => i !== index))} />
              </li>
            ))}
          </ul>
        <Textarea
          size="md"
          variant="unstyled"
          autosize
          minRows={1}
          maxRows={8}
          placeholder="Summarize something ... "
          classNames={{ wrapper: 'w-full'}}
        />
        
        <div className="flex justify-between w-full">
          <MenuDropDown 
            button={
              <ActionIcon
                size={32}
                radius="xl"
                variant="transparent"
                aria-label="Upload">
                  <IconPlus size={18} stroke={1.5}></IconPlus>
              </ActionIcon>
            }
            onFileSelect={(files) => setFileArray(prev => [...prev, ...files])}
          >
          </MenuDropDown>

          <ActionIcon
            size={32}
            radius="xl"
            color={theme.primaryColor}
            variant="filled"
            aria-label="Enter"
          >
            <IconArrowRight size={18} stroke={1.5} />
          </ActionIcon>
        </div>

      </Paper>
    </Dropzone>
  );
}